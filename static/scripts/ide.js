let editor;

window.onload = function () {
  codeBuffer = document.querySelector("#bufferCode").value;
  language = document.querySelector("#languages").value;
  editor = ace.edit("editor");
  editor.setTheme("ace/theme/monokai");

  editor.setValue(codeBuffer);

  if (language === "c++") {
    editor.session.setMode("ace/mode/c_cpp");
  } else if (language === "java") {
    editor.session.setMode("ace/mode/java");
  } else if (language === "python") {
    editor.session.setMode("ace/mode/python");
  }
  editor.clearSelection(1);
};

function changeLanguage() {
  const language = document.querySelector("#languages").value;

  if (language === "c++") {
    editor.session.setMode("ace/mode/c_cpp");
    editor.setValue(
      '#include<iostream> \nusing namespace std; \nint main() \n{\n cout<<"Hello C++!";\n return 0;\n}\n'
    );
    editor.clearSelection(1);
  } else if (language === "java") {
    editor.session.setMode("ace/mode/java");
    editor.setValue(
      'public class Main {\n\tpublic static void main(String args[]) {\n\t\tSystem.out.println("Hello Java!");\n\t}\n}\n'
    );
    editor.clearSelection(1);
  } else if (language === "python") {
    editor.session.setMode("ace/mode/python");
    editor.setValue("print('Hello Python!')\n");
    editor.clearSelection(1);
  }
}

function executeCode() {
  codeBuffer = document.querySelector("#bufferCode");
  editorCode = editor.getValue();
  codeBuffer.value = editorCode;
}
