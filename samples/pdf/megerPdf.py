import os
import fitz  # PyMuPDF

def merge_pdfs(folder_path, output_path):
    # 创建 PyMuPDF 的文档对象
    merger = fitz.open()

    # 递归处理文件夹内的所有 PDF 文件
    for root, dirs, files in os.walk(folder_path):
        for pdf_file in files:
            if pdf_file.endswith('.pdf'):
                pdf_path = os.path.join(root, pdf_file)

                # 打印文件名，用于调试
                print(f'Merging: {pdf_file}')

                # 尝试打开 PDF 文件
                try:
                    pdf_document = fitz.open(pdf_path)

                    # 打印输入 PDF 文件的页面数量
                    print(f'Input PDF pages: {pdf_document.page_count}')

                    # 检查页面数量，只有当有页面时才合并
                    if pdf_document.page_count > 0:
                        merger.insert_pdf(pdf_document)

                    pdf_document.close()
                except Exception as e:
                    print(f'Error merging {pdf_file}: {e}')
                    import traceback
                    traceback.print_exc()

    # 打印合并后的文档的页面数量
    print(f'Merged PDF pages: {merger.page_count}')

    # 保存合并后的 PDF
    try:
        # 只有当合并后的文档有页面时才保存
        if merger.page_count > 0:
            merger.save(output_path)
        else:
            print('No pages to save. Merged PDF will not be created.')
    except Exception as e:
        print(f'Error saving merged PDF: {e}')
    
    merger.close()

# 指定文件夹路径和输出文件路径
folder_path = r'D:\personSpace\Math'
output_path = os.path.join(folder_path, 'merged.pdf')

# 调用合并函数
merge_pdfs(folder_path, output_path)

print(f'合并完成，输出文件保存在: {output_path}')
