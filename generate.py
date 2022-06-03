"""
Author: oitsjustjose | github.com/oitsjustjose | oitsjustjose.com
A simple UI-based generator
"""
import os
import sys

from PIL import Image


def generate(base_dir: str, overlay_dir: str, output_dir: str) -> str:
    """
    Generates the overlaid images
    Params:
        base_dir (str): the directory of the base textures
        overlay_dir (str): the directory of the overlay textures
        output_dir (str): the directory of the finished textures
    Returns:
        (str): Any errors that occurred
    """
    if not os.path.exists(base_dir):
        return "The Base Texture directory given does not exist!"
    if not os.path.exists(overlay_dir):
        return "The Overlay Texture directory given does not exist!"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    errors = []
    for base_fn in os.listdir(base_dir):
        if os.path.isdir(f"{base_dir}/{base_fn}"):
            continue
        if not base_fn.endswith(".png"):
            errors.append(f"Base texture {base_fn} is not an image. Skipping..")
            continue

        background_name = base_fn[: base_fn.rindex(".")]
        background = Image.open(f"{base_dir}/{base_fn}").convert("RGBA")

        for overlay_fn in os.listdir(overlay_dir):
            try:
                if os.path.isdir(f"{overlay_dir}/{overlay_fn}"):
                    continue
                if not overlay_fn.endswith(".png"):
                    errors.append(
                        f"Overlay texture {overlay_fn} is not an image. Skipping.."
                    )
                    continue

                overlay = Image.open(f"{overlay_dir}/{overlay_fn}")
                Image.alpha_composite(background, overlay).save(
                    f"{output_dir}/{background_name}_{overlay_fn}"
                )
            except ValueError as err:
                errors.append(
                    f"Failed to generate bedtexture with {base_fn} background and {overlay_fn} overlay"
                )
                errors.append(err)
                continue

    return "\n".join(errors)


def headless() -> None:
    """
    A headless version of the app
    """

    def __help():
        print("Usage for Headless Mode:")
        print(
            "    generate --headless --base-layer-dir=<BASE_LAYER_DIR> --overlay-layer-dir=<OVERLAY_LAYER_DIR> --output-dir=<OUTPUT_DIR>"
        )
        sys.exit(1)

    if "-help" in sys.argv or "-h" in sys.argv or "?" in sys.argv:
        __help()

    base_dir = ""
    overlay_dir = ""
    output_dir = ""

    try:
        for arg in sys.argv:
            if arg.startswith("--base-layer-dir"):
                base_dir = arg.split("=")[1]
            if arg.startswith("--overlay-layer-dir"):
                overlay_dir = arg.split("=")[1]
            if arg.startswith("--output-dir"):
                output_dir = arg.split("=")[1]
    except:
        __help()
    if not base_dir or not overlay_dir or not output_dir:
        __help()

    msgs = generate(base_dir, overlay_dir, output_dir)
    if msgs:
        print(msgs)
    else:
        print(
            "Successfully generated textures! Check your output directory to see the results."
        )


def gui() -> None:
    """
    The GUI-based version of the app :)
    Imports for GUI-based logic are done here as a result
    """
    import PySimpleGUI as sg

    sg.theme("SystemDefaultForReal")

    base_dir = ""
    overlay_dir = ""
    output_dir = ""

    content = [
        [
            sg.Text("Base Layer Folder"),
            sg.In(size=(25, 1), enable_events=True, key="-BASE LAYERS-"),
            sg.FolderBrowse(),
        ],
        [
            sg.Text("Overlay Layer Folder"),
            sg.In(size=(25, 1), enable_events=True, key="-OVERLAY LAYERS-"),
            sg.FolderBrowse(),
        ],
        [
            sg.Text("Output Directory"),
            sg.In(size=(25, 1), enable_events=True, key="-OUTPUT DIR-"),
            sg.FolderBrowse(),
        ],
        [sg.Button("Start", key="-START-", disabled=True)],
    ]

    # ----- Full layout -----
    layout = [[sg.Column(content, justification="center")]]
    window = sg.Window("MOTG", layout, element_justification="center")

    # Run the Event Loop
    while True:
        event, values = window.read()
        can_start = base_dir and overlay_dir and output_dir

        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "-BASE LAYERS-":
            base_dir = values["-BASE LAYERS-"]
            can_start = base_dir and overlay_dir and output_dir
            window["-START-"].update(disabled=not can_start)
        if event == "-OVERLAY LAYERS-":
            overlay_dir = values["-OVERLAY LAYERS-"]
            can_start = base_dir and overlay_dir and output_dir
            window["-START-"].update(disabled=not can_start)
        if event == "-OUTPUT DIR-":
            output_dir = values["-OUTPUT DIR-"]
            can_start = base_dir and overlay_dir and output_dir
            window["-START-"].update(disabled=not can_start)
        if event == "-START-":
            if base_dir and overlay_dir and output_dir:
                try:
                    msgs = generate(base_dir, overlay_dir, output_dir)
                    if msgs:
                        sg.popup_error(msgs)
                    else:
                        sg.popup_quick_message(
                            "Successfully generated textures! Check your output directory to see the results.",
                            title="Success!",
                        )
                except Exception as err:
                    sg.popup_error_with_traceback(msgs, err)

    window.close()


if __name__ == "__main__":
    if sys.argv[1:]:
        headless()
    else:
        gui()
