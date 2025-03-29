import gradio as gr
import os
import tempfile
import shutil
import cv2

from face2face import Face2Face
from media_toolkit import VideoFile

f2f = Face2Face()

def imgswap(source_path, target_path, enhance=False, output_folder='output_folder'):
    enhance_model = 'gpen_bfr_2048' if enhance else None
    os.makedirs(output_folder, exist_ok=True)
    swapped_img = f2f.swap_img_to_img(source_path, target_path, enhance_face_model=enhance_model)
    output_path = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(target_path))[0]}_swapped.jpg")
    cv2.imwrite(output_path, cv2.cvtColor(swapped_img, cv2.COLOR_RGB2BGR))
    return output_path

def multi_vidswap(source_path, target_paths, enhance=False, output_folder='output_folder'):
    enhance_model = 'gpen_bfr_2048' if enhance else None
    source_img = cv2.imread(source_path)
    f2f.add_face("caprio", source_img, save=True)
    os.makedirs(output_folder, exist_ok=True)
    output_files = []
    for target_path in target_paths:
        vf = VideoFile().from_file(target_path)
        swapped = f2f.swap(media=vf, faces="caprio", enhance_face_model=enhance_model)
        output_path = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(target_path))[0]}_swapped.mp4")
        swapped.save(output_path)
        output_files.append(output_path)
    return output_files

def handle_swap(mode, source_img, targets, enhance):
    if source_img is None or targets is None or (isinstance(targets, list) and len(targets) == 0):
        return "❌ Please upload both source and target files.", None

    with tempfile.TemporaryDirectory() as tmpdir:
        source_path = os.path.join(tmpdir, "source.jpg")
        cv2.imwrite(source_path, source_img)

        if mode == "Image":
            target_path = os.path.join(tmpdir, "target.jpg")
            cv2.imwrite(target_path, targets)
            output_path = imgswap(source_path, target_path, enhance)
            return "✅ Image Swap Complete", [output_path]

        elif mode == "Multi Video":
            video_paths = []
            for target in targets:
                target_path = os.path.join(tmpdir, os.path.basename(target.name))
                shutil.copy(target.name, target_path)
                video_paths.append(target_path)
            output_paths = multi_vidswap(source_path, video_paths, enhance)
            return "✅ Multi-Video Swap Complete", output_paths

    return "❌ Something went wrong.", None

def build_ui():
    with gr.Blocks(title="Face Swap Tool") as demo:
        gr.Markdown("## Face Swap Tool with Image & Video\nUpload a source face image and a target. Works for images and multi videos!")

        with gr.Row():
            mode = gr.Radio(["Image", "Multi Video"], label="Select Mode", value="Image")

        with gr.Row():
            source_input = gr.Image(label="Source Face Image", type="numpy")

        target_input_image = gr.Image(label="Target Image", type="numpy", visible=True)
        target_input_multivideo = gr.File(file_types=[".mp4"], label="Multiple Target Videos", file_count="multiple", visible=False)

        enhance_toggle = gr.Checkbox(label="Enhance Face Quality", value=False)

        swap_button = gr.Button("Run Face Swap 🚀")
        output_status = gr.Textbox(label="Status", interactive=False)
        output_gallery = gr.Gallery(label="Output Files", show_label=True, columns=2)

        # Update visibility based on mode
        def update_inputs(mode):
            return {
                target_input_image: gr.update(visible=(mode == "Image")),
                target_input_multivideo: gr.update(visible=(mode == "Multi Video")),
            }

        mode.change(fn=update_inputs, inputs=mode, outputs=[target_input_image, target_input_multivideo])

        def launch_swap(mode, source_img, image_input, multivideo_input, enhance):
            if mode == "Image":
                return handle_swap(mode, source_img, image_input, enhance)
            elif mode == "Multi Video":
                return handle_swap(mode, source_img, multivideo_input, enhance)

        swap_button.click(
            fn=launch_swap,
            inputs=[mode, source_input, target_input_image, target_input_multivideo, enhance_toggle],
            outputs=[output_status, output_gallery]
        )

    return demo

if __name__ == "__main__":
    ui = build_ui()
    ui.launch(server_name="0.0.0.0", server_port=7860)
