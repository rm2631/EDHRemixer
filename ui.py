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

    # Initialize collections in session state
    if "collections" not in st.session_state:
        st.session_state["collections"] = []
    collections = st.session_state["collections"]

    # Split layout into two columns
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("Engine & Add Collection")
        st.subheader("Add New Collection")
        name = st.text_input("Name")
        url = st.text_input("URL")
        is_source = st.checkbox("Is Source")
        btn_col1, btn_col2 = st.columns([1, 1])
        add_clicked = btn_col1.button("Add Collection")
        run_clicked = btn_col2.button("Run Engine")
        if add_clicked:
            new_collection = {"name": name, "url": url, "is_source": is_source}
            collections.append(new_collection)
            st.session_state["collections"] = collections
            st.success("Collection added successfully!")
        if run_clicked:
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
    with col2:
        st.header("Collections List")
        for i, collection in enumerate(collections):
            st.write(f"{i + 1}. Name: {collection['name']}, URL: {collection['url']}, Is Source: {collection['is_source']}")
            if st.button(f"Delete {collection['name']}", key=f"delete_{i}"):
                collections.pop(i)
                st.session_state["collections"] = collections
                st.success(f"Deleted {collection['name']}")
                st.rerun()

if __name__ == "__main__":
    main()