# RZNPy: A Python Client for the Rzn Tauri Application
=====================================================

RZNPy is a lightweight Python client library designed to interact with the Rzn Tauri application. It provides a simple and intuitive interface to query and manage your local files and folders indexed by the Rzn app.

**What is Rzn?**
----------------

Rzn is a powerful tool that allows you to add folders on your local machine and automatically syncs data in those folders. It indexes all data into three types of indexes: keyword, BM25, and semantic search. You can choose your embedding model for the semantic index and set the required dimensions within the application. The app handles new files and folders added or removed, making it easy to manage your data.

**Features of RZNPy**
--------------------

RZNPy enables you to:

* Query data in specific indexes (keyword, BM25, semantic) or use the composite search to query all indexes together.
* Optionally use the re-ranking feature, which leverages open source re-ranker models to re-rank results.
* Perform fast search queries, even over thousands of documents.
* Interact with your local files while maintaining an index on selected documents.
* Use the library for local retrieval on your machines.

**Getting Started**
-------------------

To use RZNPy, you need to have the Rzn Tauri application installed and running on your machine. You can download the Rzn app from the [Reason homepage](https://rzn.ai).

**Installation**
--------------

To install RZNPy, run the following command in your terminal:

```
pip install rznpy
```

**Examples**
----------

Here are some examples to get you started with RZNPy:

### Initialize the Client

```python
from rznpy import RZNClient

client = RZNClient(host="localhost", port=9928)
```

### Get Projects

```python
projects = client.get_projects(offset=0, limit=10)
print(projects)
```

### Get Added Folders

```python
folders = client.get_added_folders()
print(folders)
```

### Get Folder Contents

```python
contents = client.get_folder_contents(parent_path="/path/to/your/folder")
print(contents)
```

### Search

```python
results = client.search(query="example query", search_type="composite", limit=10, rerank=True)
print(results)
```

**Feedback and Support**
-------------------------

For any feedback or support, please write to [feedback@rzn.ai](mailto:feedback@rzn.ai).

**License**
---------

RZNPy is licensed under the MIT License.
