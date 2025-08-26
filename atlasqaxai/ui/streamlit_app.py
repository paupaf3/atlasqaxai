import streamlit as st
import io
import contextlib

from atlasqaxai.commands import ingest, rebuild, wipe, inspect, ask, summary


def initialize_chat_with_summary():
    """Initialize chat with a welcome message including index summary."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Add initial summary message if chat is empty
    if not st.session_state.messages:
        index_summary = summary.get_summary()
        st.session_state.messages.append({
            "role": "assistant",
            "content": index_summary
        })


def main():
    st.set_page_config(
        page_title="AtlasQAX.ai",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("AtlasQAX.ai")
    st.markdown("*Intelligent Question Answering from Multiple Data Sources*")

    # Sidebar for system management
    with st.sidebar:
        st.header("System Management")

        if st.button("🔄 Rebuild Index", help="Rebuild the entire index from scratch", use_container_width=True):
            with st.spinner("Rebuilding index..."):
                try:
                    rebuild.run()
                    st.success("Index rebuilt successfully!")
                    # Refresh the chat with new summary after rebuild
                    st.session_state.messages = []
                    initialize_chat_with_summary()
                except Exception as e:
                    st.error(f"Error rebuilding index: {e}")

        if st.button("📥 Ingest Documents", help="Index new/changed documents", use_container_width=True):
            with st.spinner("Ingesting documents..."):
                try:
                    ingest.run()
                    st.success("Documents ingested successfully!")
                    # Refresh the chat with new summary after ingestion
                    st.session_state.messages = []
                    initialize_chat_with_summary()
                except Exception as e:
                    st.error(f"Error ingesting documents: {e}")

        if st.button("🔍 Inspect Index", help="Inspect the current index", use_container_width=True):
            with st.spinner("Inspecting index..."):
                try:
                    # Capture the output of inspect.run()
                    import io
                    import contextlib

                    f = io.StringIO()
                    with contextlib.redirect_stdout(f):
                        inspect.run()
                    output = f.getvalue()
                    st.text_area("Index Information", output, height=200)
                except Exception as e:
                    st.error(f"Error inspecting index: {e}")

        if st.button("📓 Refresh Summary", help="Refresh the document summary in chat", use_container_width=True):
            # Clear chat and re-initialize with fresh summary
            st.session_state.messages = []
            initialize_chat_with_summary()
            st.success("Summary refreshed!")

        if st.button("🗑️ Wipe Index", help="Delete the entire index", use_container_width=True):
            if st.session_state.get('confirm_wipe', False):
                try:
                    wipe.run()
                    st.success("Index wiped successfully!")
                    # Clear chat and show empty index message after wipe
                    st.session_state.messages = []
                    initialize_chat_with_summary()
                    st.session_state.confirm_wipe = False
                except Exception as e:
                    st.error(f"Error wiping index: {e}")
            else:
                st.session_state.confirm_wipe = True
                st.warning(
                    "Click again to confirm deletion of the entire index!")

    # Initialize chat history with summary
    initialize_chat_with_summary()

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = ask.run(prompt)
                    answer = str(response.content)
                    st.markdown(answer)

                    # Add assistant response to chat history
                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer})

                except Exception as e:
                    error_msg = f"Error processing question: {e}"
                    st.error(error_msg)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_msg})

    # Clear chat history button
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        initialize_chat_with_summary()  # Re-add the summary after clearing
        st.rerun()


if __name__ == "__main__":
    main()
