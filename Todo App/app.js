// ELEMENTS & VARIABLES
var addBox = document.querySelector("#todo-add-box");
var addButton = document.querySelector("#add-button");
var searchBox = document.querySelector("#search");
var todoList = document.querySelector("#todo-list-ul");
var doneAllButton = document.querySelector("#done-all-button");
let list = [];

// INITIALS
dataCheck();
reconstructTodos();
var doneButtons = Array.from(document.querySelectorAll(".done-button"));

// FUNCTIONS
function dataCheck() {
    localStorage.getItem("todos") == null ? list = [] : list = JSON.parse(localStorage.getItem("todos"));
}

function reconstructTodos() {
    for (var i = 0; i < list.length; i++)
        UIaddTodo(list[i]);
}

function refreshEvents() {
    doneButtons = Array.from(document.querySelectorAll(".done-button"));
    for (let i = 0; i < doneButtons.length; i++) 
        doneButtons[i].addEventListener("click", doneTodo);
}

function constructTodo(todoName) {
    let newTodo = document.createElement("li");
    newTodo.className = "list-group-item d-flex justify-content-between mx-5 my-2";
    todoName = todoName.trim();
    let doneButton = document.createElement("button");
    doneButton.className = "btn btn-success done-button";
    doneButton.type = "button";
    doneButton.innerHTML = "Done";
    newTodo.appendChild(document.createTextNode(todoName));
    newTodo.appendChild(doneButton);
    return newTodo;
}

function UIaddTodo(todoName) {
    todoList.appendChild(constructTodo(todoName));
    return todoName;
}

function addBoxControl(e) {
    if (addBox.value.trim() == "Don't forget to name your todo!") {
        addBox.value = "";
        addBox.style.color = "#fff"
    }
    e.preventDefault();
}

function addTodo(e) {
    if (addBox.value.trim() == "") {
        addBox.style.color = "#ae2012";
        addBox.value ="Don't forget to name your todo!";
        e.preventDefault();
    }
    else {
        list.push(UIaddTodo(addBox.value));
        localStorage.setItem("todos", JSON.stringify(list));
        console.log("Task added: " + addBox.value);
        addBox.value = "";
        refreshEvents();
        e.preventDefault();
    }
}

function doneTodo(e) {
    let element = e.target;
    let toBeGone = "";
    for (let i = 0; i < element.parentElement.textContent.length - 4; i++)
        toBeGone += element.parentElement.textContent[i];
    list.splice(list.indexOf(toBeGone), 1);
    element.parentElement.remove();
    localStorage.setItem("todos", JSON.stringify(list));
    console.log("Task Deleted: "+toBeGone);
    refreshEvents();
    e.preventDefault();
}

function filterTodos(e) {
    document.querySelectorAll(".list-group-item").forEach(function (listItem) {
        listItem.textContent.toLowerCase().indexOf(e.target.value.toLowerCase()) == -1 ? listItem.setAttribute("style", "display: none !important") : listItem.setAttribute("style", "display: flex !important");
    });
}

function doneAll(e) {
    document.querySelectorAll(".list-group-item").forEach(function (listItem) {
        listItem.remove();
    });
    localStorage.clear();
    console.log("Tasks all cleared.");
    refreshEvents();
    e.preventDefault();
}



// EVENT LISTENERS
addBox.addEventListener("click", addBoxControl);
addButton.addEventListener("click", addTodo);
doneAllButton.addEventListener("click", doneAll);
searchBox.addEventListener("keyup",filterTodos);
refreshEvents();

