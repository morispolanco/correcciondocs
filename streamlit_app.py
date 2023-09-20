import streamlit as st
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.dml import MSO_THEME_COLOR_INDEX
from docx.shared import Pt
from translate import Translator
from difflib import ndiff

def translate_text(text, dest):
    translator = Translator(to_lang=dest)
    translation = translator.translate(text)
    return translation

def compare_documents(original_doc, translated_doc):
    changes_doc = Document()
    
    for orig_paragraph, trans_paragraph in zip(original_doc.paragraphs, translated_doc.paragraphs):
        orig_text = orig_paragraph.text
        trans_text = trans_paragraph.text
        
        if orig_text != trans_text:
            changes_paragraph = changes_doc.add_paragraph()
            
            for diff in ndiff(orig_text, trans_text):
                if diff.startswith('-'):
                    run = changes_paragraph.add_run(diff[2:])
                    run.font.color.theme_color = MSO_THEME_COLOR_INDEX.RED
                    run.font.size = Pt(12)
                elif diff.startswith('+'):
                    run = changes_paragraph.add_run(diff[2:])
                    run.font.color.theme_color = MSO_THEME_COLOR_INDEX.GREEN
                    run.font.size = Pt(12)
                else:
                    run = changes_paragraph.add_run(diff[2:])
                    run.font.size = Pt(12)
        
    return changes_doc

def main():
    st.title("Aplicación de Traducción y Control de Cambios")
    
    # Cargar el documento original
    original_doc_path = st.file_uploader("Cargar documento original (.docx)", type="docx")
    
    if original_doc_path is not None:
        original_doc = Document(original_doc_path)
        
        # Obtener el idioma de destino
        dest_lang = st.selectbox("Seleccionar idioma de destino", ["en", "fr", "de", "it"])
        
        # Traducir el documento original
        translated_doc = Document()
        
        for orig_paragraph in original_doc.paragraphs:
            translated_text = translate_text(orig_paragraph.text, dest_lang)
            translated_paragraph = translated_doc.add_paragraph(translated_text)
            translated_paragraph.style = orig_paragraph.style
            translated_paragraph.alignment = orig_paragraph.alignment
        
        # Comparar los documentos original y traducido
        changes_doc = compare_documents(original_doc, translated_doc)
        
        # Descargar el documento con control de cambios
        st.download_button("Descargar documento con control de cambios", data=changes_doc.save("changes_document.docx"), file_name="changes_document.docx")
    
if __name__ == "__main__":
    main()
