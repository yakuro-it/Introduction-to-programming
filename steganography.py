import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

END_MARKER = "<<<END>>>"

def text_to_bits(text: str) -> list[int]:
    data = text.encode("utf-8")
    bits = []
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits

def bits_to_text(bits: list[int]) -> str:
    if len(bits) % 8 != 0:
        bits = bits[: len(bits) - (len(bits) % 8)]
    data = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for b in bits[i:i+8]:
            byte = (byte << 1) | b
        data.append(byte)
    return data.decode("utf-8", errors="ignore")

def capacity_bits(img: Image.Image) -> int:
    w, h = img.size
    return w * h * 3  # 1 bit per RGB channel

def encode_image(input_path: str, output_path: str, message: str) -> None:
    img = Image.open(input_path).convert("RGB")
    msg = message + END_MARKER
    msg_bits = text_to_bits(msg)

    cap = capacity_bits(img)
    if len(msg_bits) > cap:
        raise ValueError(f"Message too large for this image.\nNeed {len(msg_bits)} bits, but image holds {cap} bits.")

    pixels = list(img.getdata())
    new_pixels = []
    bit_i = 0

    for (r, g, b) in pixels:
        if bit_i < len(msg_bits):
            r = (r & 0xFE) | msg_bits[bit_i]
            bit_i += 1
        if bit_i < len(msg_bits):
            g = (g & 0xFE) | msg_bits[bit_i]
            bit_i += 1
        if bit_i < len(msg_bits):
            b = (b & 0xFE) | msg_bits[bit_i]
            bit_i += 1
        new_pixels.append((r, g, b))

    out = Image.new("RGB", img.size)
    out.putdata(new_pixels)
    out.save(output_path)

def decode_image(input_path: str) -> str:
    img = Image.open(input_path).convert("RGB")
    pixels = list(img.getdata())

    bits = []
    for (r, g, b) in pixels:
        bits.append(r & 1)
        bits.append(g & 1)
        bits.append(b & 1)

    collected = []
    for i in range(0, len(bits), 8):
        chunk = bits[i:i+8]
        if len(chunk) < 8:
            break
        collected.extend(chunk)
        text = bits_to_text(collected)
        if END_MARKER in text:
            return text.split(END_MARKER)[0]

    return ""


class StegoGUI:
    def __init__(self, root):
        self.root = root
        root.title("Secret Message Hider (Steganography)")
        root.geometry("650x450")

        self.in_path = tk.StringVar()
        self.out_path = tk.StringVar()

        tk.Label(root, text="Input PNG Image:").pack(anchor="w", padx=10, pady=(10, 0))
        f1 = tk.Frame(root)
        f1.pack(fill="x", padx=10)
        tk.Entry(f1, textvariable=self.in_path).pack(side="left", fill="x", expand=True)
        tk.Button(f1, text="Browse", command=self.browse_input).pack(side="left", padx=5)

        tk.Label(root, text="Output PNG Image (for encode):").pack(anchor="w", padx=10, pady=(10, 0))
        f2 = tk.Frame(root)
        f2.pack(fill="x", padx=10)
        tk.Entry(f2, textvariable=self.out_path).pack(side="left", fill="x", expand=True)
        tk.Button(f2, text="Save As", command=self.save_output).pack(side="left", padx=5)

        tk.Label(root, text="Message to Hide:").pack(anchor="w", padx=10, pady=(10, 0))
        self.msg_box = tk.Text(root, height=6)
        self.msg_box.pack(fill="both", expand=False, padx=10)

        btns = tk.Frame(root)
        btns.pack(fill="x", padx=10, pady=10)
        tk.Button(btns, text="Encode (Hide Message)", command=self.encode).pack(side="left")
        tk.Button(btns, text="Decode (Extract Message)", command=self.decode).pack(side="left", padx=10)
        tk.Button(btns, text="Clear", command=self.clear).pack(side="left")

        tk.Label(root, text="Output / Extracted Message:").pack(anchor="w", padx=10, pady=(10, 0))
        self.out_box = tk.Text(root, height=8)
        self.out_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def browse_input(self):
        path = filedialog.askopenfilename(
            title="Select PNG Image",
            filetypes=[("PNG Images", "*.png"), ("All Files", "*.*")]
        )
        if path:
            self.in_path.set(path)

    def save_output(self):
        path = filedialog.asksaveasfilename(
            title="Save Encoded Image As",
            defaultextension=".png",
            filetypes=[("PNG Images", "*.png")]
        )
        if path:
            self.out_path.set(path)

    def encode(self):
        inp = self.in_path.get().strip()
        out = self.out_path.get().strip()
        msg = self.msg_box.get("1.0", "end").strip()

        if not inp:
            messagebox.showerror("Error", "Please choose an input PNG image.")
            return
        if not out:
            messagebox.showerror("Error", "Please choose an output PNG file name (Save As).")
            return
        if not msg:
            messagebox.showerror("Error", "Please type a message to hide.")
            return

        try:
            encode_image(inp, out, msg)
            messagebox.showinfo("Success", f"Message hidden successfully! and Saved")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decode(self):
        inp = self.in_path.get().strip()
        if not inp:
            messagebox.showerror("Error", "Please choose an image to decode.")
            return

        try:
            msg = decode_image(inp)
            self.out_box.delete("1.0", "end")
            if msg:
                self.out_box.insert("1.0", msg)
            else:
                self.out_box.insert("1.0", "No hidden message found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear(self):
        self.msg_box.delete("1.0", "end")
        self.out_box.delete("1.0", "end")


if __name__ == "__main__":
    root = tk.Tk()
    app = StegoGUI(root)
    root.mainloop()

