# SABIO BACKEND DATA SPECIFICATION



# Dataset CSV


|               | ID                               | StartDate          | EndDate                                                      | DateString                                                                                  | Title                     | Description                         | ObjectURLSuffix                                                                                                                                | ObjectParameter1                                                             | ... | ObjectParameterN                                                             |
|---------------|----------------------------------|--------------------|--------------------------------------------------------------|---------------------------------------------------------------------------------------------|---------------------------|-------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------|-----|------------------------------------------------------------------------------|
| dtype         | int                              | string             | string                                                       | string                                                                                      | string                    | string                              | string/int                                                                                                                                     | string                                                                       | ... | string                                                                       |
| unique values | True                             | False              | False                                                        | False                                                                                       | False                     | False                               | True                                                                                                                                           | False                                                                        | ... | False                                                                        |
| description   | will be used as index into table | format: yyyy-mm-dd | format: yyyy-mm-dd; set equal to StartDate if not applicable | display date in interface, displayed as-is; if empty, string will be 'StartDate -- EndDate' | display name in interface | displayed as part of object details | object's reference string/number/ID that will be added as a suffix to the object_base_url in the NMvW dataset ; this field is the same as 'ID' | optional; used as additional parameter to restrict search (e.g. categorical) | ... | optional; used as additional parameter to restrict search (e.g. categorical) |
|               |                                  |                    |                                                              |                                                                                             |                           |                                     |                                                                                                                                                |                                                                              |     |                                                                              |




# Meta JSON

dict with items:

 - id: the dataset's ID, will be used in the backend as a key for index (i.e. should be hashable & unique)
 
 - name: the dataset's display name, that is displayed in the frontend (doesn't need to be unique)
 
 - source_url: the URL of the dataset's website; e.g. the landing page for the public search interface in the case of the NMvW dataset
 
 - object_base_url: the URL prefix for providing links to the native collection API; in the backend, this link will be suffixed by the objects' URL identifiers as provided in the column 'ObjectURLSuffix'; e.g. for the NMvW dataset this link is https://hdl.handle.net/20.500.11840/ which is suffixed by ojects' ID (e.g. https://hdl.handle.net/20.500.11840/653099 for the object with ID 653099)
 
 - text_columns: names of columns in the dataset CSV to be used in the backend for search and scoring; object's Titles and Descriptions are used by default (i.e. if text_columns is an empty list, Titles and Descriptions will be used); in the backend, the columns' values will be joined by "\n" for searching and scoring

 - dataset_params: a dict with the names of columns in the CSV which are to be used as search parameters as keys and, as values, the information on such parameters required to instantiate datasets.DatasetParameter objects (as a dict); see the class definition for possible values and how they are used in the backend

