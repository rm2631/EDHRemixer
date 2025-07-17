import streamlit as st

st.set_page_config(layout="wide")
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

    # Handle form reset flag before rendering widgets
    if st.session_state.get("reset_form", False):
        st.session_state["name"] = ""
        st.session_state["url"] = ""
        st.session_state["is_source"] = False
        st.session_state["reset_form"] = False
        st.rerun()

    # Split layout into two columns
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("Add New Collection")
        name = st.text_input("Name", value=st.session_state.get("name", ""), key="name")
        url = st.text_input("URL", value=st.session_state.get("url", ""), key="url")
        is_source = st.checkbox(
            "Is a Source?",
            value=st.session_state.get("is_source", False),
            key="is_source",
        )
        btn_col1, btn_col2 = st.columns([1, 1])
        add_clicked = btn_col1.button("Add Collection")
        run_clicked = btn_col2.button("Run Engine")
        if add_clicked:
            new_collection = {
                "name": st.session_state["name"],
                "url": st.session_state["url"],
                "is_source": st.session_state["is_source"],
            }
            collections.append(new_collection)
            st.session_state["collections"] = collections
            st.session_state["reset_form"] = True
            st.success("Collection added successfully!")
            st.rerun()
        if run_clicked:
            try:
                from main import run

                output_file = run(collections)
                st.download_button(
                    label="Download Excel File",
                    data=output_file,
                    file_name="reshuffled.xlsx",  # You can set a static or dynamic filename
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
                st.success("Engine ran successfully! You can download the file above.")
            except Exception as e:
                st.error(f"Error running the engine: {e}")
    with col2:
        st.header("Collections List")
        # Add header row for grid
        header_cols = st.columns([2, 4, 2, 1])
        header_cols[0].markdown("**Name**")
        header_cols[1].markdown("**URL**")
        header_cols[2].markdown("**Type**")
        header_cols[3].markdown("**Delete**")
        # Display each collection in a horizontally aligned row
        for i, collection in enumerate(collections):
            grid_cols = st.columns([2, 4, 2, 1])
            grid_cols[0].write(collection["name"])
            grid_cols[1].write(collection["url"])
            grid_cols[2].write("Source" if collection["is_source"] else "Target")
            delete_icon = "🗑️"
            if grid_cols[3].button(delete_icon, key=f"delete_{i}"):
                collections.pop(i)
                st.session_state["collections"] = collections
                st.success(f"Deleted {collection['name']}")
                st.rerun()


if __name__ == "__main__":
    main()
