"use client"; // this line is necessary if you're using Next.js 13+ to use client-side rendering

import React, { useState, useRef, useCallback } from "react";
import Webcam from "react-webcam";

const Page = () => {
    const webcamRef = useRef(null);
    const [imageSrc, setImageSrc] = useState(null);

    // Configure video constraints for the webcam
    const videoConstraints = {
        width: 1280,
        height: 720,
        facingMode: "user", // Use "environment" for back camera on mobile devices
    };

    // Function to capture the image from webcam
    const capture = useCallback(() => {
        const imageSrc = webcamRef.current.getScreenshot();
        setImageSrc(imageSrc);
    }, [webcamRef]);

    return (
        <div style={{ textAlign: "center", marginTop: "50px" }}>
            <h1 style={{ marginBottom: "30px" }}>Handwriting Recognition</h1> {/* Added margin-bottom */}
            <Webcam
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                videoConstraints={videoConstraints}
                style={{
                    width: "100%",
                    maxWidth: "640px",
                    marginBottom: "20px",
                }}
            />
            <div style={{ width: "700px", margin: "0 auto", textAlign: "center" }}>
                <p
                    style={{
                        fontFamily: "Arial, sans-serif",
                        fontSize: "24px",
                        letterSpacing: "2px",
                        textAlign: "center", // Center the text inside the paragraph
                    }}
                >
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
                    finibus aliquam ante, mattis viverra ex sodales et. Fusce
                    placerat ullamcorper metus, eu tristique odio hendrerit at.
                    Donec ac felis ac ipsum accumsan pharetra eget quis enim. Ut
                    dolor nibh, egestas ac felis nec, lacinia auctor quam. Sed
                    tempor luctus lorem, quis molestie ligula aliquet ut.
                </p>
            </div>
        </div>
    );
};

export default Page;
