import { Paper } from "@mui/material";
import React from "react";

export function PdfUpload({
  onUpload,
}: {
  onUpload: (file: File | null) => void;
}) {
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files ? event.target.files[0] : null;
    if (file) {
      console.log(file);
      const formData = new FormData();
      formData.append("the_file", file);

      fetch("http://127.0.0.1:5000/uploadPDF", {
        method: "POST",
        body: formData,
      })
        .then((response) => {
          if (response.ok) {
            console.log("File uploaded successfully");
          } else {
            console.error("Failed to upload file");
          }
        })
        .catch((error) => {
          console.error("Error uploading file:", error);
        });
    }
  };

  return (
    <Paper>
      <input type="file" accept=".pdf" onChange={handleFileChange} />
    </Paper>
  );
}
