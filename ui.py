import streamlit as st
import streamlit.components.v1 as components

# JavaScript code for interacting with browser local storage
local_storage_js = """
<script>
function saveToLocalStorage(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
}

function loadFromLocalStorage(key) {
    const value = localStorage.getItem(key);
    return value ? JSON.parse(value) : null;
}

function deleteFromLocalStorage(key) {
    localStorage.removeItem(key);
}
</script>
"""

# Inject JavaScript into the Streamlit app
components.html(local_storage_js, height=0)

# Streamlit UI
def main():
    st.title("Collection Manager")

    # Add a button to run the engine
    if st.button("Run Engine"):
        try:
            from main import run
            output_file = run(collections)

            with open(output_file, "rb") as file:
                st.download_button(
                    label="Download Excel File",
                    data=file,
                    file_name=output_file,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            st.success("Engine ran successfully! You can download the file above.")
        except Exception as e:
            st.error(f"Error running the engine: {e}")

    # Load existing collections from browser local storage
    collections = st.experimental_get_query_params().get("collections", [])

    # Display collections
    st.subheader("Current Collections")
    for collection in collections:
        st.write(f"Name: {collection['name']}, URL: {collection['url']}, Is Source: {collection['is_source']}")

    # Add a new collection
    st.subheader("Add New Collection")
    name = st.text_input("Name")
    url = st.text_input("URL")
    is_source = st.checkbox("Is Source")

    if st.button("Add Collection"):
        new_collection = {"name": name, "url": url, "is_source": is_source}
        collections.append(new_collection)
        st.experimental_set_query_params(collections=collections)
        st.success("Collection added successfully!")

    # Edit or delete collections
    st.subheader("Manage Collections")
    for i, collection in enumerate(collections):
        st.write(f"{i + 1}. {collection['name']} ({collection['url']})")
        if st.button(f"Delete {collection['name']}"):
            collections.pop(i)
            st.experimental_set_query_params(collections=collections)
            st.success(f"Deleted {collection['name']}")

if __name__ == "__main__":
    main()