<p:declare-step xmlns:p="http://www.w3.org/ns/xproc" version="1.0"
                name="simple-pipeline">
  <p:input port="source"/>
  <p:output port="result">
    <p:pipe step="xinclude" port="result"/>
  </p:output>
  <p:xinclude name="xinclude"/>
  <p:xslt name="make-clean">
    <p:input port="stylesheet">
      <p:inline>
        <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                        version="2.0">
          <xsl:template match="/">
            <html><head><title>Cleaned up</title></head>
            <body><xsl:apply-templates/></body>
            </html>
          </xsl:template>
          <xsl:template match="para">
            <p><xsl:apply-templates/></p>
          </xsl:template>
        </xsl:stylesheet>
      </p:inline>
    </p:input>
  </p:xslt>
</p:declare-step>