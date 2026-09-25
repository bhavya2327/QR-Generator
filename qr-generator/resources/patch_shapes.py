import re

with open('src/app/page.js', 'r') as f:
    text = f.read()

# 1. Update State Variables
text = text.replace(
    "const [styleShape, setStyleShape] = useState('square');",
    "const [bodyShape, setBodyShape] = useState('square');\n    const [eyeFrameShape, setEyeFrameShape] = useState('square');\n    const [eyeBallShape, setEyeBallShape] = useState('square');"
)

# 2. Update Bulk Generation Options
text = text.replace(
    "dotsOptions: { color: fgColor, type: styleShape === 'dot' ? 'dots' : styleShape === 'round' ? 'rounded' : 'square' },",
    "dotsOptions: { color: fgColor, type: bodyShape },\n                    cornersSquareOptions: { color: fgColor, type: eyeFrameShape },\n                    cornersDotOptions: { color: fgColor, type: eyeBallShape },"
)

# 3. Update Customization UI Section
custom_ui = """
                        <div className="mb-3">
                            <label htmlFor="body_shape" className="text-muted mb-2">Body Shape</label>
                            <select id="body_shape" className="form-control" value={bodyShape} onChange={(e) => setBodyShape(e.target.value)}>
                                <option value="square">Square</option>
                                <option value="dots">Dots</option>
                                <option value="rounded">Rounded</option>
                                <option value="extra-rounded">Extra Rounded</option>
                                <option value="classy">Classy</option>
                                <option value="classy-rounded">Classy Rounded</option>
                            </select>
                        </div>
                        <div className="mb-3">
                            <label htmlFor="eye_frame_shape" className="text-muted mb-2">Eye Frame Shape</label>
                            <select id="eye_frame_shape" className="form-control" value={eyeFrameShape} onChange={(e) => setEyeFrameShape(e.target.value)}>
                                <option value="square">Square</option>
                                <option value="dot">Dot</option>
                                <option value="extra-rounded">Extra Rounded</option>
                            </select>
                        </div>
                        <div className="mb-3">
                            <label htmlFor="eye_ball_shape" className="text-muted mb-2">Eye Ball Shape</label>
                            <select id="eye_ball_shape" className="form-control" value={eyeBallShape} onChange={(e) => setEyeBallShape(e.target.value)}>
                                <option value="square">Square</option>
                                <option value="dot">Dot</option>
                            </select>
                        </div>
"""
text = re.sub(
    r'<label htmlFor="qr_style" className="text-muted mb-2">QR Code Style</label>.*?</div>',
    custom_ui,
    text,
    flags=re.DOTALL
)

# 4. Update Props to QRCodePreview
text = text.replace(
    "styleShape={styleShape}",
    "bodyShape={bodyShape} eyeFrameShape={eyeFrameShape} eyeBallShape={eyeBallShape}"
)

# 5. Update Props to handleSingleDownload
text = text.replace(
    "styleShape, null",
    "bodyShape, eyeFrameShape, eyeBallShape, null"
)

with open('src/app/page.js', 'w') as f:
    f.write(text)

