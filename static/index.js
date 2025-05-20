async function download() {
    const url = document.getElementById("urlInput").value;
    const filename = document.getElementById("playListName").value;

    if (!url) {
        alert("Please enter a playlist URL.");
        return;
    }
    if (!filename) {
        alert("Please enter a the playlist name.");
        return;
    }

    try{
        const response = await fetch('api/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({url, filename})
        });

        const data = await response.json();

        if (!response.ok){
            throw new Error(data.message || 'Something went wrong ask Kai');
            alert("Download failed: " + data.message);
        }

        alert("Download started successfully!");
    }
        catch (error) {
        console.error("Error:", error);
            alert("An error occurred: " + error.message);
        }
}