module fts.FileTreeWalker

import java.nio.file.Path
import java.nio.file.Files
import java.nio.file.FileVisitor
import java.nio.file.SimpleFileVisitor
import java.nio.file.FileVisitResult
import java.nio.file.attribute.BasicFileAttributes

# Walks a file tree from a root path.
#
# The walk is controlled by a visitor that has the following functions:
#
# - `onFile(path, attributes)`
# - `onDirectory(path, attributes)`
# - `onVisitFileFailed(path, exception)`
# - `onPreVisitDirectory(path, attributes)`
# - `onPostVisitDirectory(path, exception)`
#
# Each of these functions is optional. They all shall return one of:
#
# - `FileVisitResult.CONTINUE`
# - `FileVisitResult.TERMINATE`
# - `FileVisitResult.SKIP_SUBTREE`
# - `FileVisitResult.SKIP_SIBLINGS`
#
# The default return value is `FileVisitResult.CONTINUE`.
#
# The visitor can be given as a map, for instance:
#
# ----
# var visitor = map[
#   ["onFile", |path, attrs| {
#     println(path)
#     return FileVisitResult.CONTINUE
#   }]
# ]
# ----
#
# It can also be an object with the corresponding methods.
#
function walk = |root, visitor| {

  var visitorAdapter = object: SimpleFileVisitor<Path>() {

    function preVisitDirectory = |path, attrs| {
      if visitor: has("onPreVisitDirectory") {
        return visitor: onPreVisitDirectory(path, attrs)
      }
      return FileVisitResult.CONTINUE
    }

    function postVisitDirectory = |path, exc| {
      if visitor: has("onPostVisitDirectory") {
        return visitor: onPostVisitDirectory(path, exc)
      }
      return FileVisitResult.CONTINUE
    }

    function visitFile = |path, attrs| {
      if visitor: has("onFile") {
        return visitor: onFile(path, attrs)
      }
      return FileVisitResult.CONTINUE
    }

    function visitFileFailed = |path, exc| {
      if visitor: has("onVisitFileFailed") {
        return visitor: onVisitFileFailed(path, exc)
      }
      return FileVisitResult.CONTINUE
    }
  }
  Files.walkFileTree(root, visitorAdapter)
}