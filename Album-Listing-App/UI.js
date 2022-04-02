class UI {

    constructAlbum(album) {
        let element = document.createElement("tr");
        element.classList.add("album-list-tr");
        element.innerHTML = `
               <td class="align-middle"><img src="${album.art}" alt="Album Image" class="img-fluid img-thumbnail w-25"></td>
               <td class="align-middle"> ${album.artist} </td>
               <td class="align-middle"> ${album.title} </td>
               <td class="align-middle delete-button"><a class="btn btn-outline-secondary btn-sm mx-0">Delete</td>
               `
        return element;
    }

    addAlbum(newAlbum) {
        document.getElementById("album-list").appendChild(this.constructAlbum(newAlbum));
        this.clearInputs();
    }

    removeAll() {
        let allAlbums = Array.from(document.querySelectorAll(".album-list-tr"));
        for (let i = 0; i < allAlbums.length; i++)
            allAlbums[i].remove();
    }

    removeAlbum(toBeGone) {
        document.getElementById("album-list").removeChild(this.constructAlbum(toBeGone));
    }

    clearInputs() {
        artistName.value = "";
        albumTitle.value = "";
        albumArt.value = "";
    }

    reconstructAlbums() {
        for (var i = 0; i < albumList.length; i++)
            this.addAlbum(albumList[i]);
    }

    isEmpty(artist, title, art) {
        if (title == "" || artist == "" || art == "") {
            if (artist == "") {
                artistName.classList.add("text-danger");
                artistName.value = "Do not forget to enter artist name!";
            }
            if (title == "") {
                albumTitle.classList.add("text-danger");
                albumTitle.value = "Do not forget to enter album title!";
            }
            if (art == "") {
                albumArt.classList.add("text-danger");
                albumArt.value = "Do not forget to enter album art link!";
            }
            return true;
        }
        else
            return false;
    }

}
