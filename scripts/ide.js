let editor;

window.onload = function () {
  editor = ace.edit("editor");
  editor.setTheme("ace/theme/monokai");
  editor.session.setMode("ace/mode/c_cpp");
};

function changeLanguage() {
  const language = document.querySelector("#languages").value;

  if (language === "c++") {
    editor.session.setMode("ace/mode/c_cpp");
  } else if (language === "java") {
    editor.session.setMode("ace/mode/java");
  } else if (language === "python") {
    editor.session.setMode("ace/mode/python");
  }
}
