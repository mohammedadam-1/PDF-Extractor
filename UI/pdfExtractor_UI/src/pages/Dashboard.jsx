import React from 'react'
import "./Dashboard.css"

function Dashboard() {
    const [fileUploaded, setFileUploaded] = React.useState(null)
    const [status, setStatus] = React.useState('Idle')
    const [result, setResult] = React.useState(null)

    const handleFileChange = (e) => {
        setFileUploaded(e.target.files[0] ?? null)
        setResult(null)
        setStatus("Idle")
    }

    const handleSubmit = async (e) => {
        e.preventDefault()

        if (!fileUploaded) return

        try {
            setStatus("Uploading")

            const formData = new FormData()
            formData.append('file', fileUploaded)

            const res = await fetch('/uploadfile', {
                method: 'POST',
                body: formData,
            })

            if (!res.ok) {
                throw new Error(`Upload failed: ${res.status}`)
            }

            const blob = await res.blob()

            const contentDisposition =
                res.headers.get('Content-Disposition')

            let filename = 'result.csv'

            if (contentDisposition) {
                const match =
                    contentDisposition.match(/filename="?([^"]+)"?/)

                if (match) {
                    filename = match[1]
                }
            }

            setResult({
                blob,
                filename
            })

            // You were missing this
            setStatus("Success")

        } catch (error) {
            console.error(error)
            setStatus("Error")
        }
    }

    const handleDownload = () => {
        if (!result) return

        // result.blob, not result
        const url = URL.createObjectURL(result.blob)

        const link = document.createElement('a')
        link.href = url
        link.download = result.filename

        document.body.appendChild(link)
        link.click()
        link.remove()

        URL.revokeObjectURL(url)
    }

    return (
        <div className='dashboard-site'>
            <p>Upload pdf file</p>

            <div className='dashboard-site__upload-file'>
                <form onSubmit={handleSubmit}>
                    <label htmlFor="file-upload">
                        Upload file here
                    </label>

                    <input
                        type="file"
                        id="file-upload"
                        accept=".pdf"
                        name="file"
                        onChange={handleFileChange}
                    />

                    <button
                        type="submit"
                        disabled={!fileUploaded || status === "Uploading"}
                    >
                        {status === 'Uploading'
                            ? 'Uploading...'
                            : 'Upload'}
                    </button>
                </form>

                {status === 'Success' && (
                    <p>
                        Upload successful! You can now download the result.
                    </p>
                )}

                {status === 'Error' && (
                    <p role="alert">
                        Something went wrong. Try again.
                    </p>
                )}
            </div>

            <div className='dashboard-site__download-file'>
                <p>Download File by clicking below!</p>

                <button
                    onClick={handleDownload}
                    disabled={!result}
                >
                    Download File
                </button>
            </div>
        </div>
    )
}

export default Dashboard