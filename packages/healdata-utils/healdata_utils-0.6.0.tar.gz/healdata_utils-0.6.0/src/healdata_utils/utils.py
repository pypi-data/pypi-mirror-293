""" General utilities/helper functions"""
import re
from collections.abc import MutableMapping
import pandas as pd
from pandas.api.types import is_object_dtype

def _get_propnames_to_rearrange(propnames,schema):
    """ 
    get data dictionary props to search for refactoring or embedding
    
    Supports patternProperties
    """

    annotation_names = ["title","description","name","additionalDescription"]
    root_names = flatten_properties(schema["properties"]).keys()
    field_names = flatten_properties(schema["properties"]["fields"]["items"]["properties"]).keys()
    props_to_rearrange = set(root_names).intersection(field_names).difference(annotation_names)

    propnames_exp = "|".join("^"+name+"$" for name in props_to_rearrange)
    names_to_rearrange = [name for name in propnames if re.match(propnames_exp,name)]

    return list(names_to_rearrange)

def embed_data_dictionary_props(flat_fields,flat_root,schema):
    """ 
    Embed (flattened) root level props in each (flattened) field
    if field level prop is missing but the field level prop exists
    and is not an annotation property (title,description). 
    
    Params
    
    flat_fields: array of dicts or pd.DataFrame (or something that can be converted into DataFrame)
    flat_root: dict or pd.Series or something that can be converted into Series 
    schema: schema for determining what fields should be embedded (note, this is flattened in fxn)
    
    Returns
    
    pd.DataFrame with the flat fields with the embedded root properties
    """
    flat_fields = pd.DataFrame(flat_fields)
    propnames = _get_propnames_to_rearrange(list(flat_root.keys()),schema)
    flat_root = pd.Series(flat_root).loc[propnames] # take out annotation props
    if len(flat_root) > 0:
        for propname in propnames:
            if propname in flat_root:
                if not propname in flat_fields:
                    flat_fields.insert(0,propname,flat_root[propname])
                else:
                    flat_fields[propname].fillna(flat_root[propname],inplace=True)

    return flat_fields

def refactor_field_props(flat_fields,schema):
    """ 
    given a flattened array of dicts corresponding to the unflattened schema,
    move up (ie `refactor`) flattened properties that are both in the root 
    (ie table level; level up from field records) and in the fields.

    """  
    flat_fields_df = pd.DataFrame(flat_fields)
    propnames = set(_get_propnames_to_rearrange(flat_fields_df.columns.tolist(),schema))
    flat_record = pd.Series(dtype="object")
    for name in propnames:
        in_df = name in flat_fields_df
        if in_df:
            # need to handle if some values are pandas series
            if isinstance(flat_fields_df[name], pd.DataFrame):
                is_one_unique = (flat_fields_df[name].nunique() == 1).all()
            elif isinstance(flat_fields_df[name], pd.Series):
                if is_object_dtype(flat_fields_df[name]):
                    is_one_unique = len(flat_fields_df[name].map(str).unique()) == 1
                else:
                    is_one_unique = flat_fields_df[name].nunique() == 1
            if is_one_unique:
                flat_record[name] = flat_fields_df.pop(name).iloc[0]
                if isinstance(flat_record[name], pd.Series):
                    flat_record[name] = flat_record[name].to_list()
            

    return flat_record,flat_fields_df

# individual cell utilities
def strip_html(html_string):
    if html_string:
        return re.sub(r"<[^>]+>", "", html_string)
    else:
        return html_string


def to_int_if_base10(val):
    """
    converts value to a string and if
    float (or a string rep of a float) of base10
    to an integer string representation.

    NOTE:
    """
    string = str(val)

    if "." in string:
        parts = string.split(".")
        if len(parts) == 2 and parts[1] == "0":
            return parts[0]

    return string


def parse_dictionary_str(string, item_sep, keyval_sep):
    """
    parses a stringified dictionary into a dictionary
    based on item separator

    """
    if string != "" and string != None:
        stritems = string.strip().split(item_sep)
        items = {}

        for stritem in stritems:
            if stritem:
                item = stritem.split(keyval_sep, 1)
                items[item[0].strip()] = item[1].strip()
        
        return items
    else:
        return string


def parse_list_str(string, item_sep):
    if string != "" and string != None:
        return string.strip().split(item_sep)
    else:
        return string


# dictionary utilities
def flatten_to_jsonpath(dictionary,schema,parent_key=False, sep="."):
    """
    Turn a nested dictionary into a flattened dictionary (but see schema param)

    :param dictionary: The dictionary to flatten
    :param schema: The schema to indicate which properties to flatten
        This includes dictionaries (properties) with child dictionaries (properties)
        and lists (items) with child dictionaries (properties)
    :param parent_key: The string to prepend to dictionary's keys
    :param sep: The string used to separate flattened keys 
    :return: A flattened dictionary
    """
    # flatten if type array -> type object with properties
    # flatten if type object with properties
    items = []
    for key, value in dictionary.items():
        new_key = str(parent_key) + sep + key if parent_key else key
        prop = schema["properties"].get(key,{})
        childprops = prop.get("properties")
        childitem_props = prop.get("items",{}).get("properties")

        if childitem_props:
            for i,_value in enumerate(value):
                item = flatten_to_jsonpath(
                    dictionary=_value, 
                    schema=prop,
                    parent_key=new_key, 
                    sep=f"[{str(i)}]{sep}")
                items.extend(item.items())
        elif childprops:
            item = flatten_to_jsonpath(
                dictionary=value, 
                schema=prop,
                parent_key=new_key, 
                sep=sep)
            items.extend(item.items())

        else:
            items.append((new_key, value))

    return dict(items)

def stringify_keys(dictionary):
    orig_keys = list(dictionary.keys())
    for key in orig_keys:
        dictionary[str(key)] = dictionary.pop(key)


def unflatten_from_jsonpath(field):
    """
    Converts a flattened dictionary with key names conforming to 
    JSONpath notation to the nested dictionary format.
    """
    field_json = {}

    for prop_path, prop in field.items():
        prop_json = field_json

        nested_names = prop_path.split(".")
        for prop_name in nested_names[:-1]:
            if '[' in prop_name:
                array_name, array_index = prop_name.split('[')
                array_index = int(array_index[:-1])
                if array_name not in prop_json:
                    prop_json[array_name] = [{} for _ in range(array_index + 1)]
                elif len(prop_json[array_name]) <= array_index:
                    prop_json[array_name].extend([{} for _ in range(array_index - len(prop_json[array_name]) + 1)])
                prop_json = prop_json[array_name][array_index]
            else:
                if prop_name not in prop_json:
                    prop_json[prop_name] = {}
                prop_json = prop_json[prop_name]

        last_prop_name = nested_names[-1]
        if '[' in last_prop_name:
            array_name, array_index = last_prop_name.split('[')
            array_index = int(array_index[:-1])
            if array_name not in prop_json:
                prop_json[array_name] = [{} for _ in range(array_index + 1)]
            elif len(prop_json[array_name]) <= array_index:
                prop_json[array_name].extend([{} for _ in range(array_index - len(prop_json[array_name]) + 1)])
            if isinstance(prop_json[array_name][array_index], dict):
                prop_json[array_name][array_index].update({array_name: prop})
            else:
                prop_json[array_name][array_index] = {array_name: prop}
        else:
            prop_json[last_prop_name] = prop

    return field_json
    
# json to csv utils
def join_iter(iterable,sep_list="|"):
    return sep_list.join([str(p) for p in iterable])

def join_dictvals(dictionary:dict,sep:str):
    return sep.join(dictionary.values())

def join_dictitems(dictionary:dict,sep_keyval='=',sep_items='|'):
    """ joins a mappable collection (ie dictionary) into a string
    representation with specified separators for the key and value
    in addition to items. 

    All items are coerced to the string representation (eg if key or value
    is None, this will be coerced to "None")


    """
    dict_list = []
    for key,val in dictionary.items():
        keystr = str(key)
        valstr = str(val)
        dict_list.append(keystr+sep_keyval+valstr)
    return sep_items.join(dict_list)


# documentation building utilities
def find_docstring_desc(fxn):
    """
    return the description part of a docstring
    (ie text before Parameters)
    """
    exp = "^(.*)Parameters\\n"

    if fxn.__doc__:
        docstring = fxn.__doc__.strip()
    else:
        docstring = "No documentation"
    try:
        return re.search(exp, docstring, re.DOTALL).group(1)
    except AttributeError:
        return docstring


# add missing values and order according to the order of a list


def sync_fields(data, field_list,missing_value=None):
    """
    Sorts fields and adds missing fields (with None value).
    If extra fields exist in a record that are not in field_list, then tacks on at 
    end of record.


    Parameters
    --------------
    data [list]: json array of values
    field_list [list]: the list of all field names  (e.g., propertjies from a schema)

    Returns
    -------------
    list: json array with fields added if missing
    """
    data_with_missing = []

    for record in data:
        new_record = {}
        for fieldpropname in field_list:
            # check if the fieldname is a property (or could be a pattern property)
            fieldnames = re.findall("|".join("^"+fieldname+"$" for fieldname in record),fieldpropname)
            # if match then add to new record
            if fieldnames:
                for name in fieldnames:
                    new_record[name] = record[name]
            # if no record than add missing value (if there is a regex list index, then add [0])
            else:
                extra_fieldname = (
                    fieldpropname
                    .replace("^","")
                    .replace("$","")
                    .replace("\[\d+\]","[0]")
                ) #replace list item regex
                new_record[extra_fieldname] = missing_value

        # tack on extra fields not in field_list at back
        extra_fields = list(set(list(record)).difference(list(new_record)))
        for name in extra_fields:
            new_record[name] = record[name]

        # append the newly synced record with missing values
        data_with_missing.append(new_record)

    
    return data_with_missing


# %% 
# Working with schemas
def flatten_properties(properties, parentkey="", sep=".",itemsep="\[\d+\]"):
    """
    flatten schema properties
    """
    properties_flattened = {}
    for key, item in properties.items():
        # flattened keys
        if parentkey:
            flattenedkey = parentkey + "." + key
        else:
            flattenedkey = key

        if isinstance(item, MutableMapping):
            props = item.get("properties")
            items = item.get("items",{}).get("properties")
            if props:
                newprops = flatten_properties(props, parentkey=flattenedkey)
                properties_flattened.update(newprops)

            elif items:
                newprops = flatten_properties(items,parentkey=flattenedkey+itemsep)
                properties_flattened.update(newprops)
            else:
                properties_flattened[flattenedkey] = item
        
        else:
            properties_flattened[flattenedkey] = item
    
    return properties_flattened

def flatten_schema(schema):
    """ 
    Flatten a schema of type object with properties. 
    
    If a regular expression indicating a list index exists, puts this
    under `patternProperties`
    
    """ 
    schema_flattened = dict(schema)
    if "properties" in schema:
        properties = schema_flattened.pop("properties")
        item_sep = "\[\d+\]"
        schema_flattened["properties"] = flatten_properties(properties,itemsep=item_sep)
        schema_flattened["patternProperties"] = {}
        for propname in list(schema_flattened["properties"].keys()):
            if item_sep in propname:
                # TODO: put on table level for csv schema
                # var0 = propname.replace(item_sep,"[0]")
                # var1 = propname.replace(item_sep,"[1]")
                # var2 = propname.replace(item_sep,"[2]")
                # pattern_property_note = (
                #     "\n\n"
                #     "Specifying field names:\n\n"
                #     "This field can have 1 or more columns using the digit index number in brackets (`[0]` --> `[1]` --> `[n]`)\n\n"
                #     "For 1 value, you will have the field (column) names:\n"
                #     "`{0}`\n\n"
                #     # "\tFor 2 values, you will have the columns: "
                #     # "`{0},`{1}`\n"
                #     "For 3 values, you will have the field (column) names:\n"
                #     "`{0}`\t`{1}`\t`{2}`\n\n"
                # ).format(var0,var1,var2)
                pattern_property_note = ""
                pattern_prop = schema_flattened["properties"].pop(propname)
                pattern_prop["description"] = pattern_prop.get("description","") + pattern_property_note
                schema_flattened["patternProperties"]["^"+propname+"$"] = pattern_prop

    return schema_flattened





def find_propname(colname,properties):
    """ 
    given a dictionary of json schema object properties OR a list of property names, return the 
    matching property name. 

    This function is needed when a schema is flattened according to a json path 
    and converted into a regular expression for list (array) indices.

    """ 
    propmatch = []
    for name in list(properties):
        if re.match("^"+name+"$",colname):
            propmatch.append(name)

    if len(propmatch) == 1:
        return propmatch[0]
    elif len(propmatch) > 1:
        raise Exception(f"Multiple matching properties found for {colname}. Can only have one match")
    elif len(propmatch) == 0:
        return None
    else:
        raise Exception(f"Unknown error when matching properties against {colname}")