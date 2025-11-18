import streamlit as st
from main import run, get_deck_name

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

    # Form section at the top
    st.subheader("Add New Collection")
    form_cols = st.columns([5, 1, 1])
    with form_cols[0]:
        url = st.text_input("URL", value=st.session_state.get("url", ""), key="url")
    with form_cols[1]:
        add_clicked = st.button(
            "Add Collection", use_container_width=True, key="add_collection"
        )
    with form_cols[2]:
        run_clicked = st.button("Reshuffle", use_container_width=True, key="run_engine")

    # Handle Add Collection button click
    if add_clicked:
        if not st.session_state["url"].strip():
            st.error("URL cannot be empty.")
        elif "moxfield" not in st.session_state["url"]:
            st.error("URL must be a valid Moxfield URL.")
        else:
            new_collection = {
                "name": get_deck_name(st.session_state["url"]),
                "url": st.session_state["url"],
                "is_source": True,  # Default to True (source)
            }
            collections.append(new_collection)
            st.session_state["collections"] = collections
            st.session_state["reset_form"] = True
            st.success("Collection added successfully!")
            st.rerun()

    # Handle Reshuffle button click
    if run_clicked:
        if not collections:
            st.error("No collections to process. Please add some first.")
        elif not any(c["is_source"] for c in collections):
            st.error("At least one collection must be a source.")
        elif not any(not c["is_source"] for c in collections):
            st.error("At least one collection must be a target.")
        else:
            try:
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

    # Collections grid section below
    st.divider()
    st.subheader("Collections")

    # Initialize sort settings in session state
    if "sort_column" not in st.session_state:
        st.session_state["sort_column"] = None
    if "sort_ascending" not in st.session_state:
        st.session_state["sort_ascending"] = True

    # Add header row for grid with sorting controls
    header_cols = st.columns([2, 4, 2, 1])

    # Create clickable headers for sorting
    with header_cols[0]:
        if st.button("▲▼ Name", key="sort_name", use_container_width=True):
            if st.session_state["sort_column"] == "name":
                st.session_state["sort_ascending"] = not st.session_state[
                    "sort_ascending"
                ]
            else:
                st.session_state["sort_column"] = "name"
                st.session_state["sort_ascending"] = True
            st.rerun()

    with header_cols[1]:
        if st.button("▲▼ URL", key="sort_url", use_container_width=True):
            if st.session_state["sort_column"] == "url":
                st.session_state["sort_ascending"] = not st.session_state[
                    "sort_ascending"
                ]
            else:
                st.session_state["sort_column"] = "url"
                st.session_state["sort_ascending"] = True
            st.rerun()

    with header_cols[2]:
        if st.button("▲▼ Type", key="sort_type", use_container_width=True):
            if st.session_state["sort_column"] == "type":
                st.session_state["sort_ascending"] = not st.session_state[
                    "sort_ascending"
                ]
            else:
                st.session_state["sort_column"] = "type"
                st.session_state["sort_ascending"] = True
            st.rerun()

    header_cols[3].markdown("**Delete**")

    # Sort collections based on current sort settings
    sorted_collections = collections.copy()
    if st.session_state["sort_column"] == "name":
        sorted_collections.sort(
            key=lambda x: x["name"].lower(),
            reverse=not st.session_state["sort_ascending"],
        )
    elif st.session_state["sort_column"] == "url":
        sorted_collections.sort(
            key=lambda x: x["url"].lower(),
            reverse=not st.session_state["sort_ascending"],
        )
    elif st.session_state["sort_column"] == "type":
        sorted_collections.sort(
            key=lambda x: x["is_source"], reverse=not st.session_state["sort_ascending"]
        )

    # Display each collection in a horizontally aligned row
    for i, collection in enumerate(sorted_collections):
        # Find original index for proper key management
        original_index = collections.index(collection)
        grid_cols = st.columns([2, 4, 2, 1])
        grid_cols[0].write(collection["name"])
        # Make URL clickable as a markdown link
        grid_cols[1].markdown(f"[{collection['url']}]({collection['url']})")
        # Allow in-place editing of Type with a selectbox
        type_options = ["Source", "Target"]
        current_type = "Source" if collection["is_source"] else "Target"
        selected_type = grid_cols[2].selectbox(
            "Type",
            options=type_options,
            index=type_options.index(current_type),
            key=f"type_{original_index}",
            label_visibility="collapsed",
        )
        # Update collection if type changed
        new_is_source = selected_type == "Source"
        if new_is_source != collection["is_source"]:
            collections[original_index]["is_source"] = new_is_source
            st.session_state["collections"] = collections
            st.rerun()

        delete_icon = "🗑️"
        if grid_cols[3].button(delete_icon, key=f"delete_{original_index}"):
            collections.pop(original_index)
            st.session_state["collections"] = collections
            st.success(f"Deleted {collection['name']}")
            st.rerun()


if __name__ == "__main__":
    main()
