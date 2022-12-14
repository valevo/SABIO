# SABIO BACKEND DATA SPECIFICATION


The SABIO backend requires the following input data structure, separated into 3 files:


# Meta JSON

The meta file declaring meta-properties of the dataset, such as its name and own URL, as well as (part of the) semantics: (1) properties of objects used for filtering and sorting them and (2) textual properties of objects that will be used for keyword search and scoring by the SABIO algorithms.

The meta file is a JSON dict with the following items:

 - `id`: the dataset's ID, will be used in the backend as a key for index (i.e. should be hashable & unique)
 
 - `name`: the dataset's display name, that is displayed in the frontend (doesn't need to be unique)
 
 - `dataset_url`: the URL of the dataset's website; e.g. the landing page for the public search interface in the case of the NMvW dataset
  

 - `dataset_params`: a dict where the keys are the names of columns in the dataset CSV which are to be used as search and sort parameters; the dict's values are themselves dicts which contain the information required to instantiate [datasets.DatasetParameter](https://github.com/valevo/SABIO/blob/b572559343fd259aa374eecf03156bd974fff449/backend/v0_8/src/datasets.py#L205) Python objects (see the class definition for possible values and how they are used in the backend)

- `text_columns`: names of columns in the dataset CSV to be used in the backend for search and scoring; objects' `name` and `description` fields are used by default (text_columns may be an empty list); in the backend, the columns' values will be joined by "\n" for searching and scoring (which affects neither search results nor scores)



# Dataset CSV

This is the main data table and needs to contain at least the following fields. Fields that are not declared as `dataset_params` or `text_colums` in the meta JSON (see above) are simply ignored. 


|               | ID                               | start_date         | end_date                                                | date_string                                                                                                        | name                      | description                         | <object_parameter_1>                                                          | ... | <object_parameter_n>                                                          | <text_column_1>                                         | ... | <text_column_m>                                         |
|---------------|----------------------------------|--------------------|---------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|---------------------------|-------------------------------------|-----------------------------------------------------------------------------|-----|-----------------------------------------------------------------------------|-------------------------------------------------------|-----|-------------------------------------------------------|
| dtype         | int                              | ISO date           | ISO date                                                | string                                                                                                             | string                    | string                              | any                                                                         | ... | any                                                                         | str                                                   | ... | str                                                   |
| unique values | True                             | False              | False                                                   | False                                                                                                              | False                     | False                               | False                                                                       | ... | False                                                                       | False                                                 | ... | False                                                 |
| description   | will be used as index into table | format: yyyy-mm-dd | format: yyyy-mm-dd; if empty, will be set to start_date | display date in interface, displayed as-is (no required format); if empty, string will be 'start_date -- end_date' | display name in interface | displayed as part of object details | optional; may be additional parameter to filter and sort (e.g. categorical) | ... | optional; may be additional parameter to filter and sort (e.g. categorical) | optional; may be additional field to filter and score | ... | optional; may be additional field to filter and score |
|               |                                  |                    |                                                         |                                                                                                                    |                           |                                     |                                                                             |     |                                                                             |                                                       |     |                                                       |


# Image CSV

The CSV holding URLs of images for objects. These URLs are simply passed to the front-end, where they are inserted into the user interface when hovering or clicking on objects. The SABIO backend therefore also works without images but this CSV is still required. So if no images are available, simply fill this CSV with placeholders (such as "").

|               | ID                               | thumbnail_URL                                 | img_URL                                                |
|---------------|----------------------------------|-----------------------------------------------|--------------------------------------------------------|
| dtype         | int                              | URL                                           | URL                                                    |
| unique values | True                             | False                                         | False                                                  |
| description   | will be used as index into the dataset CSV | passed as-is to the front-end; shown on hover | passed as-is to the front-end; shown in object details |
|               |                                  |                                               |                                                        |
