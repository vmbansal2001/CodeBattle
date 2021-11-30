let editor;
// let input;

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
};

function changeLanguage() {
  const language = document.querySelector("#languages").value;

  if (language === "c++") {
    editor.session.setMode("ace/mode/c_cpp");
    // document.querySelector("#editor").textContent =
    //   "#include<iostream> using namespace std; int main() {return 0; }";    //didn't work
    editor.setValue(
      "#include<iostream> \nusing namespace std; \nint main() \n{\n return 0;\n}\n"
    );
  } else if (language === "java") {
    editor.session.setMode("ace/mode/java");
    editor.setValue(
      'public class Main {\n\tpublic static void main(String args[]) {\n\t\tSystem.out.println("Hello World!");\n\t}\n}\n'
    );
    // input = editor.getValue();
    // console.log(input); // to get value
  } else if (language === "python") {
    editor.session.setMode("ace/mode/python");
    editor.setValue("print('Hello World')\n");
  }
}

function executeCode(){
  codeBuffer = document.querySelector("#bufferCode");
  editorCode = editor.getValue();
  codeBuffer.value = editorCode;
}
