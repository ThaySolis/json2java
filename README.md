This repository contains a code generator that reads an input JSON file and generates corresponding Java classes like the following example:

```json
{
  "Student": [
    {
      "name": "Bob",
      "id": "12341234",
      "phone": "9999999",
      "Course": [
        {
          "code": "CI1061",
          "name": "Embedded Systems"
        },
        {
          "code": "CI1057",
          "name": "Programming 2"
        }
      ]
    },
    {
      "name": "Alice",
      "id": "123456",
      "phone": "8888888",
      "Course": [
        {
          "code": "CI1061",
          "name": "Embedded Systems"
        },
        {
          "code": "CI1056",
          "name": "Programming 1"
        }
      ]
    }
  ]
}
```

The generated Java code based on the above JSON file is the following:

```java
import java.util.ArrayList;
class Course {
	String code;
	String name;
}
class Student {
	String name;
	String id;
	String phone;
	ArrayList<Course> course;
}
public class Program {
	public static void main (String args[]){
	}
}
```

In order to run the generator, use it as follows:

    python3 jsonToJava.py <input.json>

The program generates the Java code into the `Program.java` file, in the current directory.

# Limitations

This generator has the following limitations:
- the input file is not validated
- the names of the list fields are not pluralized
- it only accepts a subset of all JSON files - only those whose structure resamble the example in this file.

# License

This project is released under the MIT License. For more information check out the [license file](LICENSE.md).