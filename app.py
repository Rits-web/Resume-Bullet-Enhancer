import streamlit as st
from groq import Groq

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="ResumeAI | Bullet Enhancer",
    page_icon="📝",
    layout="wide"
)

# ---------------- CUSTOM STYLING ----------------

st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        color: #4F46E5;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        color: #64748b;
        margin-bottom: 30px;
    }

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 48px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown(
    '<div class="main-title">ResumeAI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Turn ordinary resume bullet points into professional, '
    'impact-focused achievements.'
    '</div>',
    unsafe_allow_html=True
)

st.info(
    "Your AI writing assistant improves clarity and impact "
    "without inventing achievements, responsibilities, or metrics."
)

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.header("⚙️ Customization")

    target_role = st.text_input(
        "Target job role",
        placeholder="e.g., Data Analyst"
    )

    experience = st.selectbox(
        "Experience level",
        [
            "Student / Fresher",
            "Intern",
            "Entry-level professional",
            "Experienced professional"
        ]
    )

    writing_style = st.selectbox(
        "Writing style",
        [
            "Professional",
            "Concise and direct",
            "Technical",
            "Leadership-focused"
        ]
    )

    number_of_versions = st.selectbox(
        "Number of versions",
        [1, 2, 3],
        index=2
    )

    st.divider()

    st.caption(
        "Powered by Streamlit and a hosted generative AI model."
    )

# ---------------- MAIN INPUT ----------------

st.subheader("✍️ Enter Your Resume Bullet Points")

st.write(
    "Paste your existing resume bullet points below. "
    "You can enter one bullet point or several."
)

resume_input = st.text_area(
    "Original resume bullet points",
    height=180,
    placeholder=(
        "Example:\n"
        "- Worked on a college website project\n"
        "- Helped organize college events\n"
        "- Used Python for data analysis"
    )
)

st.caption(
    "Tip: Include real tasks, tools, responsibilities, "
    "and results wherever possible."
)

# ---------------- AI FUNCTION ----------------

def enhance_bullet_points(
    original_text,
    target_role,
    experience,
    writing_style,
    number_of_versions
):
    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )

    prompt = f"""
You are an expert resume writer and career coach.

TASK:
Improve the user's resume bullet points.

CANDIDATE DETAILS:
Target role: {target_role or "Not specified"}
Experience level: {experience}
Preferred writing style: {writing_style}

ORIGINAL RESUME BULLET POINTS:
{original_text}

REQUIREMENTS:

1. Rewrite the bullet points to be clear, concise,
   professional, and impact-focused.

2. Use strong action verbs and relevant terminology
   appropriate to the target role.

3. Preserve the candidate's actual experience and meaning.

4. NEVER invent numbers, percentages, revenue, achievements,
   responsibilities, technologies, awards, or outcomes.

5. If the original lacks measurable results, do not fabricate
   metrics. Explain what additional truthful information
   the candidate could provide.

6. Do not claim that an activity produced a result unless
   the original information supports that claim.

7. Avoid generic claims such as "highly successful"
   unless supported by the supplied information.

8. Provide {number_of_versions} distinct version(s) for
   each original bullet point.

9. Keep the output organized and easy to compare.

10. For each original bullet point, provide:
    - Original bullet point
    - Improved version(s)
    - Why the rewrite is stronger
    - Missing information that could strengthen it,
      if applicable

11. If the input is vague, improve only what can reasonably
    be inferred and clearly identify missing information.

12. Never ask the user to include confidential information.

Use clear headings and bullet points.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful resume enhancement assistant. "
                    "Truthfulness is more important than making "
                    "a candidate sound impressive."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_completion_tokens=1800
    )

    return response.choices[0].message.content


# ---------------- GENERATE BUTTON ----------------

st.divider()

generate_button = st.button(
    "✨ Enhance My Resume",
    type="primary",
    use_container_width=True
)

if generate_button:

    if not resume_input.strip():
        st.warning(
            "Please enter at least one resume bullet point."
        )

    else:
        try:
            with st.spinner(
                "AI is improving your resume bullet points..."
            ):
                result = enhance_bullet_points(
                    resume_input,
                    target_role,
                    experience,
                    writing_style,
                    number_of_versions
                )

            st.session_state["enhanced_result"] = result
            st.session_state["original_input"] = resume_input

        except KeyError:
            st.error(
                "API key not found. Check that your "
                ".streamlit/secrets.toml file exists and "
                "contains GROQ_API_KEY."
            )

        except Exception as error:
            st.error(
                "The AI request failed. Check your internet "
                "connection, API key, model availability, "
                "and account limits."
            )

            with st.expander("Technical error details"):
                st.code(str(error))


# ---------------- DISPLAY RESULTS ----------------

if "enhanced_result" in st.session_state:

    st.subheader("📊 Enhanced Resume Bullet Points")

    st.markdown(st.session_state["enhanced_result"])

    st.divider()

    st.download_button(
        label="📥 Download Enhanced Bullet Points",
        data=st.session_state["enhanced_result"],
        file_name="enhanced_resume_bullets.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.success(
        "Review every generated bullet point before "
        "adding it to your resume. Make sure it accurately "
        "reflects your real experience."
    )


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "ResumeAI | Generative AI Jury Project | PS 87"
)