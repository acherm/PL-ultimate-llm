<%@ Language=PerlScript %>
<%
  # PerlScript ASP example: display a multiplication table
  my $size = 5;

  $Response->Write("<table border='1'>\n");
  for my $i (1 .. $size) {
    $Response->Write("<tr>\n");
    for my $j (1 .. $size) {
      my $product = $i * $j;
      $Response->Write("  <td>$product</td>\n");
    }
    $Response->Write("</tr>\n");
  }
  $Response->Write("</table>\n");
%>
