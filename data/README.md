# SABIO BACKEND DATA SPECIFICATION


The SABIO backend requires the following input data structure, separated into 3 files:




# Meta JSON

The meta file declaring meta-properties of the dataset, such as its name and own URL, as well as (part of the) semantics, on one hand of the textual properties of the objects and of properties that can be search by on the other hand.  
It is a JSON dict with the following items:

 - id: the dataset's ID, will be used in the backend as a key for index (i.e. should be hashable & unique)
 
 - name: the dataset's display name, that is displayed in the frontend (doesn't need to be unique)
 
 - dataset_url: the URL of the dataset's website; e.g. the landing page for the public search interface in the case of the NMvW dataset
  
 - text_columns: names of columns in the dataset CSV to be used in the backend for search and scoring; object's Titles and Descriptions are used by default (i.e. if text_columns is an empty list, Titles and Descriptions will be used); in the backend, the columns' values will be joined by "\n" for searching and scoring

 - dataset_params: a dict with the names of columns in the CSV which are to be used as search parameters as keys and, as values, the information on such parameters required to instantiate datasets.DatasetParameter objects (as a dict); see the class definition for possible values and how they are used in the backend



# Dataset CSV

This is the main data table and needs to contain at least the following fields. Additional fields (that are not declared as textual or search properties in the meta JSON (see above)) are simply ignored. 


|               | ID                               | start_date         | end_date                                                | date_string                                                                                                        | name                      | description                         | <object_parameter_1>                                                         | ... | <object_parameter_n>                                                         |
|---------------|----------------------------------|--------------------|---------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|---------------------------|-------------------------------------|------------------------------------------------------------------------------|-----|------------------------------------------------------------------------------|
| dtype         | int                              | ISO date           | ISO date                                                | string                                                                                                             | string                    | string                              | any                                                                          | ... | any                                                                          |
| unique values | True                             | False              | False                                                   | False                                                                                                              | False                     | False                               | False                                                                        | ... | False                                                                        |
| description   | will be used as index into table | format: yyyy-mm-dd | format: yyyy-mm-dd; if empty, will be set to start_date | display date in interface, displayed as-is (no required format); if empty, string will be 'start_date -- end_date' | display name in interface | displayed as part of object details | optional; used as additional parameter to restrict search (e.g. categorical) | ... | optional; used as additional parameter to restrict search (e.g. categorical) |
|               |                                  |                    |                                                         |                                                                                                                    |                           |                                     |                                                                              |     |                                                                              |


# Image CSV

The CSV holding URLs of images for objects. These URLs are simply passed to the front-end, where they are inserted into the user interface when hovering or clicking on objects. The SABIO interface therefore also works without images. This CSV is however still required, so if no images are available, simply fill this CSV with placeholders (such as "").

|               | ID                               | thumbnail_URL                                 | img_URL                                                |
|---------------|----------------------------------|-----------------------------------------------|--------------------------------------------------------|
| dtype         | int                              | URL                                           | URL                                                    |
| unique values | True                             | False                                         | False                                                  |
| description   | will be used as index into table | passed as-is to the front-end; shown on hover | passed as-is to the front-end; shown in object details |
|               |                                  |                                               |                                                        |