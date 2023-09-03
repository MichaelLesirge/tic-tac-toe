import 'dart:io';

String input(String prompt, {String promptPostfix = ": "}) {
  stdout.write(prompt + promptPostfix);
  String? output = stdin.readLineSync();
  return output ?? "";
}

void main() {
  String name = input("What is your name");
  print("Hello ${name}");
}
