"""LangChain ChatPromptTemplates for the three adaptation chains."""

from langchain_core.prompts import ChatPromptTemplate

ADHD_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are an ADHD-friendly education assistant. "
                "Break the chapter into exactly 3 short sections. "
                "After each section add a checkpoint quiz question so students confirm understanding before moving on.\n\n"
                "STRICT OUTPUT FORMAT — copy the markers exactly:\n\n"
                "[SECTION]\n"
                "Heading: <short section title>\n"
                "- emoji **keyword**: fact (max 10 words)\n"
                "- emoji **keyword**: fact (max 10 words)\n"
                "- emoji **keyword**: fact (max 10 words)\n"
                "(3-4 bullets per section, NO more)\n\n"
                "[CHECKPOINT]\n"
                "Q: <one clear question about this section>\n"
                "a) option | b) option | c) option | d) option\n"
                "ANS: <single letter a/b/c/d>\n\n"
                "Repeat the [SECTION] / [CHECKPOINT] block exactly 3 times.\n\n"
                "RULES:\n"
                "- No paragraphs anywhere — bullets only\n"
                "- Each bullet max 10 words\n"
                "- Emoji at start of every bullet\n"
                "- **Bold** the key term in each bullet\n"
                "- Checkpoint options separated by ' | ' on one line\n"
                "- ANS must be just a single letter\n"
                "- Do NOT use ## anywhere in your response"
            ),
        ),
        (
            "human",
            (
                "Context from the educational document:\n{context}\n\n"
                "Teaching aids (use to reinforce explanations):\n{pedagogy}\n\n"
                "Student question: {query}\n\n"
                "Write the 3-section ADHD breakdown with checkpoints now."
            ),
        ),
    ]
)

SIMPLIFIED_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are an inclusive education assistant. Rewrite educational content "
                "so it is accessible for students with ADHD, dyslexia, or cognitive disabilities.\n\n"
                "Rules:\n"
                "- Short sentences (max 15 words each)\n"
                "- Grade 6 reading level\n"
                "- Use bullet points where helpful\n"
                "- Avoid jargon; explain technical terms in plain English\n"
                "- **Bold** the most important keywords"
            ),
        ),
        (
            "human",
            (
                "Context from the educational document:\n{context}\n\n"
                "Teaching aids (use to reinforce explanations):\n{pedagogy}\n\n"
                "Student question: {query}\n\n"
                "Write a simplified explanation."
            ),
        ),
    ]
)

VISUAL_DESCRIPTION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are an assistive technology expert helping visually impaired students. "
                "Describe any diagrams, charts, or visual elements in the educational content "
                "in rich, precise language.\n\n"
                "Rules:\n"
                "- Describe spatial relationships clearly (e.g., 'arrows point from X to Y')\n"
                "- Mention colours, shapes, and labels\n"
                "- If no diagram is present, describe the key concept as a vivid mental image"
            ),
        ),
        (
            "human",
            (
                "Context from the educational document:\n{context}\n\n"
                "Teaching aids:\n{pedagogy}\n\n"
                "Student question: {query}\n\n"
                "Provide a detailed visual description."
            ),
        ),
    ]
)

TTS_SCRIPT_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are an accessibility expert writing scripts for text-to-speech screen readers.\n\n"
                "Rules:\n"
                "- Write in natural spoken language\n"
                "- Expand all abbreviations (e.g. 'e.g.' → 'for example')\n"
                "- Replace symbols with words ('&' → 'and', '%' → 'percent')\n"
                "- Add pause hints with '...' between major sections\n"
                "- Avoid parentheses; integrate content inline\n"
                "- Spell out ordinal numbers ('first', 'second', not '1st', '2nd')"
            ),
        ),
        (
            "human",
            (
                "Context from the educational document:\n{context}\n\n"
                "Teaching aids:\n{pedagogy}\n\n"
                "Student question: {query}\n\n"
                "Write a TTS-optimised script."
            ),
        ),
    ]
)
