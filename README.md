# Resolve a list of local JAR files against Maven Central.

The script calculates the SHA-1 checksum of each JAR and
matches them using Maven Central's REST web service. For
files known to the service, it prints an POM dependency
snippet, unknown files are printed for reference.

> Script modified from: https://blog.mafr.de/2016/03/20/resolving-jars/

## Usage:
  ```bash
  python3 ant2maven-dep-tool.py PATH > maven-dependancies.xml


  # ex. python3 ant2maven-dep-tool.py ~/AntProject/lib > maven-dependancies.xml

  # maven-dependancies.xml that was created

      <dependency>
        <groupId>commons-codec</groupId>
        <artifactId>commons-codec</artifactId>
        <version>1.10</version>
      </dependency>
      <dependency>
        <groupId>commons-collections</groupId>
        <artifactId>commons-collections</artifactId>
        <version>3.2.1</version>
      </dependency>
      <!--UNKNOWN JAR SHA1 - /home/someuser/AntProject/lib/mail.jar -->
  ```