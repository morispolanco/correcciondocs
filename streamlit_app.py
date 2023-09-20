import streamlit as st
from docx import Document
from googletrans import Translator
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

def translate_text(text, dest):
    translator = Translator()
    translation = translator.translate(text, dest=dest)
    return translation.text

def compare_documents(original_doc, translated_doc):
    changes_doc = Document()
    for i in range(len(original_doc.paragraphs)):
        original_text = original_doc.paragraphs[i].text
        translated_text = translated_doc.paragraphs[i].text
        if original_text != translated_text:
            p = changes_doc.add_paragraph()
            p.add_run("Original: ").bold = True
            p.add_run(original_text)
            p.add_run("\nTranslated: ").bold = True
            p.add_run(translated_text)
            p.add_run("\n\n")
    return changes_doc

def download_document(doc, filename):
    doc.save(filename)
    st.download_button("Download Changes", filename)

def main():
    st.title("Double Translation Comparison")

    # Upload the original document
    st.header("Upload Original Document")
    original_file = st.file_uploader("Upload a DOCX file", type=["docx"])
    if original_file is not None:
        original_doc = Document(original_file)

        # Translate to English
        st.header("Translate to English")
        translated_doc_en = Document()
        for paragraph in original_doc.paragraphs:
            translated_text = translate_text(paragraph.text, 'en')
            translated_doc_en.add_paragraph(translated_text)

        # Translate back to Spanish
        st.header("Translate back to Spanish")
        translated_doc_es = Document()
        for paragraph in translated_doc_en.paragraphs:
            translated_text = translate_text(paragraph.text, 'es')
            translated_doc_es.add_paragraph(translated_text)

        # Compare the documents
        st.header("Comparison")
        changes_doc = compare_documents(original_doc, translated_doc_es)
        for paragraph in changes_doc.paragraphs:
            if paragraph.text:
                st.write(paragraph.text)

        # Download the changes document
        st.header("Download Changes")
        download_document(changes_doc, "changes.docx")

if __name__ == "__main__":
    main()
