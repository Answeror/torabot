<?xml version='1.0' encoding='UTF-8'?>
<xsl:stylesheet
    version='1.0'
    xmlns:xsl='http://www.w3.org/1999/XSL/Transform'
    xmlns:re='http://exslt.org/regular-expressions'
    extension-element-prefixes='re'
>
    <xsl:output method='xml' encoding='UTF-8'/>
    <xsl:template match='/'>
        <feed xml:lang='zh-CN' xmlns='http://www.w3.org/2005/Atom'>
            <id>bgm.tv/pm</id>
            <link rel='alternate' type='text/html' href='http://bgm.tv/pm'/>
            <title>bgm.tv/pm</title>
            <xsl:apply-templates select='//table[@class="topic_list"]'/>
        </feed>
    </xsl:template>
    <xsl:template match='table'>
        <xsl:for-each select='.//tr[td[contains(@class, "pm_")]]'>
            <xsl:variable name='date' select='.//small[@class="grey"]'/>
            <xsl:variable name='year' select='re:replace($date, "(\d+)-(\d+)-(\d+)", "", "\1")'/>
            <xsl:variable name='month' select='re:replace($date, "(\d+)-(\d+)-(\d+)", "", "\2")'/>
            <xsl:variable name='day' select='re:replace($date, "(\d+)-(\d+)-(\d+)", "", "\3")'/>
            <xsl:variable name='time' select='concat($year, "-", format-number($month, "00"), "-", format-number($day, "00"), "T00:00:00Z")'/>
            <xsl:variable name='content' select='.//span[@class="tip"]'/>
            <entry>
                <id><xsl:value-of select='.//input[@type="checkbox"]/@value'/></id>
                <published><xsl:value-of select='$time'/></published>
                <updated><xsl:value-of select='$time'/></updated>
                <link rel='alternate' type='text/html'>
                    <xsl:attribute name='href'>
                        <xsl:value-of select='.//a[1]/@href'/>
                    </xsl:attribute>
                </link>
                <title><xsl:value-of select='normalize-space(.//a[1])'/></title>
                <summary><xsl:value-of select='$content'/></summary>
                <content type='text'><xsl:value-of select='$content'/></content>
                <author>
                    <name><xsl:value-of select='.//a[2]'/></name>
                    <url><xsl:value-of select='.//a[2]/@href'/></url>
                </author>
            </entry>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
