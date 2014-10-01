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
            <id>{{ id }}</id>
            <link rel='alternate' type='text/html' href='http://bgm.tv/pm'/>
            <title><xsl:value-of select='//title[1]'/></title>
            <xsl:apply-templates select='//div[@id="comment_list"]'/>
        </feed>
    </xsl:template>
    <xsl:template match='div'>
        <xsl:for-each select='.//div[contains(@id, "post_")]'>
            <xsl:variable name='date' select='.//div[@class="re_info"][1]/small/text()'/>
            <xsl:variable name='year' select='re:replace($date, "^.* - (\d+)-(\d+)-(\d+) (\d+):(\d+)[\s\S]*$", "", "\1")'/>
            <xsl:variable name='month' select='re:replace($date, "^.* - (\d+)-(\d+)-(\d+) (\d+):(\d+)[\s\S]*$", "", "\2")'/>
            <xsl:variable name='day' select='re:replace($date, "^.* - (\d+)-(\d+)-(\d+) (\d+):(\d+)[\s\S]*$", "", "\3")'/>
            <xsl:variable name='hour' select='re:replace($date, "^.* - (\d+)-(\d+)-(\d+) (\d+):(\d+)[\s\S]*$", "", "\4")'/>
            <xsl:variable name='minute' select='re:replace($date, "^.* - (\d+)-(\d+)-(\d+) (\d+):(\d+)[\s\S]*$", "", "\5")'/>
            <xsl:variable name='time' select='concat($year, "-", format-number($month, "00"), "-", format-number($day, "00"), "T", format-number($hour, "00"), ":", format-number($minute, "00"), ":00Z")'/>
            <xsl:variable name='content' select='.//div[@class="message" or @class="cmt_sub_content"][1]'/>
            <entry>
                <id><xsl:value-of select='@id'/></id>
                <published><xsl:value-of select='$time'/></published>
                <updated><xsl:value-of select='$time'/></updated>
                <link rel='alternate' type='text/html'>
                    <xsl:attribute name='href'>
                        <xsl:value-of select='.//div[@class="re_info"][1]//a[1]/@href'/>
                    </xsl:attribute>
                </link>
                <title><xsl:value-of select='normalize-space(.//div[@class="re_info"][1]//a[1])'/></title>
                <summary><xsl:value-of select='$content'/></summary>
                <content type='html'><xsl:copy-of select='$content/node()'/></content>
                <author>
                    <name><xsl:value-of select='.//div[@class="inner"]//a[1]'/></name>
                    <url><xsl:value-of select='.//div[@class="inner"]//a[1]/@href'/></url>
                </author>
            </entry>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
