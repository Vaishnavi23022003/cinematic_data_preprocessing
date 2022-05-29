# cinematic_data_preprocessing

### The data set
I have used the Movilens dataset and the files are in the `dataset` directory.

---
### movies_content_based_filtering.py
This file fetches data from the dataset and on the basis of [Content based filtering](https://developers.google.com/machine-learning/recommendation/content-based/basics) finds similar movies for all the mocies and stores them in `json_files/movie_data.json`.

---
### database_data_uploading.py
This file is used to store the data from `dataset` and `json_files` into the database.
