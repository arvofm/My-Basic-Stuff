// ELEMENTS
const artistName = document.getElementById("artist-name");
const albumTitle = document.getElementById("album-title");
const albumArt = document.getElementById("album-art-link");
const albumAddBtn = document.getElementById("add-album-button");
const removeAllBtn = document.getElementById("delete-all-button");

const ui = new UI();
const storage = new Storage();
let albumList = [];

// FUNCTIONS
function dataCheck() {
    albumList = storage.getAlbumsFromStorage();
}
function refreshEvents() {
    let deleteButtons = Array.from(document.querySelectorAll(".delete-button"));
    for (let i = 0; i < deleteButtons.length; i++)
        deleteButtons[i].addEventListener("click", deleteAlbum);
}
function init() {
    ui.clearInputs();
    dataCheck();
    ui.reconstructAlbums();
    refreshEvents();
}
function addAlbum(e) {
    let artist = artistName.value.trim();
    let title = albumTitle.value.trim();
    let art = albumArt.value.trim();

    if (!ui.isEmpty(artist, title, art)) {
        let album = new Album(artist, title, art);
        albumList.push(album);
        ui.addAlbum(album);
        storage.setItem(albumList);
        refreshEvents();
        e.preventDefault();
    }
}
function deleteAlbum(e) {
    for (let i = 0; i < albumList.length; i++)
        if (albumList[i].title == e.target.parentElement.previousElementSibling.innerHTML.trim()) {
            albumList.splice(i, 1);
            e.target.parentElement.parentElement.remove()
            storage.setItem(albumList);
            refreshEvents();
            e.preventDefault();
        }
}
function normalizeTextLabel(e) {
    if (e.target.value == "Do not forget to enter album art link!" ||
        e.target.value == "Do not forget to enter album title!" ||
        e.target.value == "Do not forget to enter artist name!") {
        e.target.classList.remove("text-danger");
        e.target.value = "";
    }
}
function deleteAll(e) {
    ui.removeAll();
    storage.clearAll();
    refreshEvents();
    e.preventDefault();
}

// LISTENERS
albumAddBtn.addEventListener("click", addAlbum);
artistName.addEventListener("click", normalizeTextLabel);
albumTitle.addEventListener("click", normalizeTextLabel);
albumArt.addEventListener("click", normalizeTextLabel);
removeAllBtn.addEventListener("click", deleteAll)

// INIT
init();
