import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="CareerPilot",
    page_icon="",
    layout="centered",
)


st.title("CareerPilot")
st.caption("Personal AI Career Agent")

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "approval_id" not in st.session_state:
    st.session_state.approval_id = None

if "approval_result" not in st.session_state:
    st.session_state.approval_result = None



with st.sidebar:
    st.header("CareerPilot")

    user_id = st.number_input(
        "User ID",
        min_value=1,
        value=1,
        step=1,
    )

    job_id = st.number_input(
        "Job ID",
        min_value=1,
        value=1,
        step=1,
    )

    st.divider()

    st.write("Backend")
    st.code(API_URL)



st.subheader("Ask CareerPilot")

request = st.text_area(
    "What would you like CareerPilot to do?",
    placeholder=(
        "Example: Analyze my fit for this job and tell me "
        "what I should do next."
    ),
    height=120,
)


if st.button(
    "Run Agent",
    type="primary",
    use_container_width=True,
):

    if not request.strip():
        st.warning("Please enter a request.")
    else:
        payload = {
            "user_id": int(user_id),
            "job_id": int(job_id),
            "request": request.strip(),
        }

        try:
            with st.spinner("CareerPilot is reasoning..."):

                response = requests.post(
                    f"{API_URL}/agent/run",
                    json=payload,
                    timeout=180,
                )

            if response.ok:
                result = response.json()

                st.session_state.last_result = result

                if result.get("approval_required"):
                    st.session_state.approval_id = result.get(
                        "tool_result",
                        {},
                    ).get("approval_id")

                else:
                    st.session_state.approval_id = None

                st.session_state.approval_result = None

            else:
                st.error(
                    f"Agent request failed: {response.status_code}"
                )
                st.code(response.text)

        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to FastAPI. "
                "Make sure the backend is running on port 8000."
            )

        except requests.exceptions.Timeout:
            st.error(
                "The agent took too long to respond."
            )

        except Exception as e:
            st.error(f"Unexpected error: {e}")



result = st.session_state.last_result


if result:

    st.divider()

    st.subheader("Agent Result")

    if result.get("error"):
        st.error(result["error"])

    else:


        st.markdown("### Decision")

        st.write(
            result.get(
                "decision",
                "No decision returned.",
            )
        )

        st.markdown("### Why")

        st.write(
            result.get(
                "explanation",
                "No explanation returned.",
            )
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Selected Tool",
                result.get(
                    "selected_tool",
                    "none",
                ),
            )

        with col2:
            approval_required = result.get(
                "approval_required",
                False,
            )

            st.metric(
                "Approval",
                "Required" if approval_required else "Not required",
            )


        skill_gaps = result.get(
            "skill_gaps",
            [],
        )

        if skill_gaps:
            st.markdown("### Skill Gaps")

            for skill in skill_gaps:
                st.write(f"- {skill}")


        tool_input = result.get(
            "tool_input",
            {},
        )

        if tool_input:
            with st.expander("Tool Input"):
                st.json(tool_input)


        tool_result = result.get(
            "tool_result",
            {},
        )

        if tool_result:
            with st.expander("Tool Result"):
                st.json(tool_result)



approval_id = st.session_state.approval_id


if approval_id:

    st.divider()

    st.subheader("Human Approval Required")

    st.warning(
        "CareerPilot wants to perform a consequential action. "
        "Review the action before allowing execution."
    )

    st.write(
        f"Approval ID: **{approval_id}**"
    )

    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "Approve",
            type="primary",
            use_container_width=True,
        ):

            try:

                with st.spinner("Approving action..."):

                    response = requests.post(
                        f"{API_URL}/approvals/"
                        f"{approval_id}/approve",
                        timeout=30,
                    )

                if response.ok:

                    st.session_state.approval_result = (
                        response.json()
                    )

                    st.success(
                        "Action approved."
                    )

                else:

                    st.error(
                        f"Approval failed: "
                        f"{response.status_code}"
                    )

                    st.code(
                        response.text
                    )

            except Exception as e:
                st.error(
                    f"Approval error: {e}"
                )


    with col2:

        if st.button(
            "Reject",
            use_container_width=True,
        ):

            try:

                with st.spinner("Rejecting action..."):

                    response = requests.post(
                        f"{API_URL}/approvals/"
                        f"{approval_id}/reject",
                        timeout=30,
                    )

                if response.ok:

                    st.session_state.approval_result = (
                        response.json()
                    )

                    st.session_state.approval_id = None

                    st.warning(
                        "Action rejected."
                    )

                else:

                    st.error(
                        f"Rejection failed: "
                        f"{response.status_code}"
                    )

                    st.code(
                        response.text
                    )

            except Exception as e:
                st.error(
                    f"Rejection error: {e}"
                )


approval_result = st.session_state.approval_result


if approval_result:

    st.divider()

    st.subheader("Approved Action")

    st.json(approval_result)

    if st.button(
        "Resume Execution",
        type="primary",
        use_container_width=True,
    ):

        try:

            with st.spinner("Executing approved action..."):

                response = requests.post(
                    f"{API_URL}/approvals/"
                    f"{approval_id}/resume",
                    timeout=180,
                )

            if response.ok:

                execution_result = response.json()

                st.success(
                    "Approved action executed successfully."
                )

                st.json(execution_result)

                st.session_state.approval_id = None

            else:

                st.error(
                    f"Execution failed: "
                    f"{response.status_code}"
                )

                st.code(
                    response.text
                )

        except Exception as e:
            st.error(
                f"Execution error: {e}"
            )