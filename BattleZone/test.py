import os, sys

code = """
public class Main {
    public static void main(String args[]) {
        System.out.println("Hello World!");
    }
}
"""

l = ["javac","-d",".", os.path.join(java_file,problemName)+".java"]