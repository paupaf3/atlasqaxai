import streamlit as st

from atlasqaxai.commands import ingest, rebuild, wipe, inspect, summary
from atlasqaxai.rag import session


def initialize_chat_with_summary():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if not st.session_state.messages:
        index_summary = summary.get_summary()
        st.session_state.messages.append({
            "role": "assistant",
            "content": index_summary,
        })


def main():
    st.set_page_config(
        page_title="AtlasQAX.ai",
        page_icon=":material/search:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("AtlasQAX.ai")
    st.markdown("*Intelligent Question Answering from Multiple Data Sources*")

    with st.sidebar:
        st.header("System Management")

        if st.button(":material/refresh: Rebuild Index", use_container_width=True):
            with st.spinner("Rebuilding index..."):
                try:
                    rebuild.run()
                    st.success("Index rebuilt successfully!")
                    st.session_state.messages = []
                    initialize_chat_with_summary()
                except Exception as e:
                    st.error(f"Error rebuilding index: {e}")

        if st.button(":material/download: Ingest Documents", use_container_width=True):
            with st.spinner("Ingesting documents..."):
                try:
                    ingest.run()
                    st.success("Documents ingested successfully!")
                    st.session_state.messages = []
                    initialize_chat_with_summary()
                except Exception as e:
                    st.error(f"Error ingesting documents: {e}")

        if st.button(":material/search: Inspect Index", use_container_width=True):
            with st.spinner("Inspecting index..."):
                try:
                    import io
                    import contextlib

                    buf = io.StringIO()
                    with contextlib.redirect_stdout(buf):
                        inspect.run()
                    st.text_area(
                        "Index Information", buf.getvalue(), height=200
                    )
                except Exception as e:
                    st.error(f"Error inspecting index: {e}")

        if st.button(":material/refresh: Refresh Summary", use_container_width=True):
            st.session_state.messages = []
            initialize_chat_with_summary()
            st.success("Summary refreshed!")

        if st.button(":material/delete: Wipe Index", use_container_width=True):
            if st.session_state.get("confirm_wipe", False):
                try:
                    wipe.run()
                    st.success("Index wiped successfully!")
                    st.session_state.messages = []
                    initialize_chat_with_summary()
                    st.session_state.confirm_wipe = False
                except Exception as e:
                    st.error(f"Error wiping index: {e}")
            else:
                st.session_state.confirm_wipe = True
                st.warning(
                    "Click again to confirm deletion of the entire index!"
                )

        st.divider()
        st.header("Query Settings")
        query_mode = st.selectbox(
            "Retrieval mode",
            options=["hybrid", "local", "global", "naive", "mix"],
            index=0,
            help=(
                "hybrid: local + global search; "
                "local: entity neighborhoods; "
                "global: global graph; "
                "naive: brute-force similarity"
            ),
        )

    initialize_chat_with_summary()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What would you like to know?"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    rag = session.get_session().get_rag()
                    answer = rag.query(prompt, mode=query_mode)

                    st.markdown(answer)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer}
                    )

                except Exception as e:
                    error_msg = f"Error processing question: {e}"
                    st.error(error_msg)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_msg}
                    )

    if st.button("Clear Chat History"):
        st.session_state.messages = []
        initialize_chat_with_summary()
        st.rerun()


if __name__ == "__main__":
    main()
