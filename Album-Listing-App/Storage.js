class Storage {
    setItem(value) {
        localStorage.setItem("Albums", JSON.stringify(value));
    }
    clearAll() {
        localStorage.clear();
    }
    removeItem(value) {
        localStorage.removeItem("Albums", value);
    }
    getAlbumsFromStorage() {
        if (localStorage.getItem("Albums") == null)
            return [];
        else
            return JSON.parse(localStorage.getItem("Albums"));
    }

}
