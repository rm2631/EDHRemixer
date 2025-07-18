import streamlit as st

st.set_page_config(layout="wide")
# ...existing code...


# Streamlit UI
def main():

    st.title("Collection Manager")
    # Initialize collections in session state at the very start
    if "collections" not in st.session_state:
        st.session_state["collections"] = []
    collections = st.session_state["collections"]

    # Handle form reset flag before rendering widgets
    if st.session_state.get("reset_form", False):
        st.session_state["name"] = ""
        st.session_state["url"] = ""
        st.session_state["reset_form"] = False
        st.rerun()

    
    # Split layout into two columns
    col1, col2 = st.columns([1, 2])

    with col1:
        st.header("Add New Collection")
        name = st.text_input("Name", value=st.session_state.get("name", ""), key="name")
        url = st.text_input("URL", value=st.session_state.get("url", ""), key="url")
        is_source = st.checkbox(
            "Is a Source?",
            value=st.session_state.get("is_source", False),
            key="is_source",
        )
        add_clicked = st.button(
            "Add Collection", use_container_width=True, key="add_collection"
        )
        if add_clicked:
            if not st.session_state["name"].strip() or not st.session_state["url"].strip():
                st.error("Name and URL cannot be empty.")
            if "moxfield" not in st.session_state["url"]:
                st.error("URL must be a valid Moxfield URL.")
            else:
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
    with col2:
        st.header("Collections List")
        head1, head2 = st.columns([1, 1])
        with head1:
            collection_popover = st.popover("Manage collections", use_container_width=True)
            # Simple import experience: use only the file uploader with a clear label
            uploaded_file = collection_popover.file_uploader(
                "Click to select a JSON file to import your collections",
                type=["json"],
                key="collections_uploader",
                label_visibility="visible",
            )
            # Use a session flag to prevent repeated imports
            if uploaded_file and not st.session_state.get("collections_imported", False):
                import json

                try:
                    imported_collections = json.load(uploaded_file)
                    if isinstance(imported_collections, list):
                        st.session_state["collections"] = imported_collections
                        st.session_state["collections_imported"] = True
                        st.rerun()
                    else:
                        st.error("Invalid format: JSON must be a list of collections.")
                except Exception as e:
                    st.error(f"Error importing collections: {e}")
            # Reset the flag if no file is uploaded
            if not uploaded_file and st.session_state.get("collections_imported", False):
                st.session_state["collections_imported"] = False
            import json
            collections_json = json.dumps(st.session_state["collections"], indent=2)
            collection_popover.download_button(
                label="Export Collections",
                data=collections_json,
                file_name="collections.json",
                mime="application/json",
                use_container_width=True,
                key="export_collections_download",
            )
        with head2:
            run_clicked = st.button(
                "Reshuffle", use_container_width=True, key="run_engine"
            )
            if run_clicked:
                if not collections:
                    st.error("No collections to process. Please add some first.")
                    return
                # the collections should contain a source and target
                if not any(c["is_source"] for c in collections):
                    st.error("At least one collection must be a source.")
                    return
                if not any(not c["is_source"] for c in collections):
                    st.error("At least one collection must be a target.")
                    return

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
