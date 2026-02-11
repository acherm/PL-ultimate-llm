{include file="header.tpl" title=foo}

<PRE>

{* block comments *}
{assign var="name" value="Bob"}

The value of $name is {$name}.

The value of $name is {$name|upper}.

{$name|upper}

{$name|spacify}

{$name|spacify:"^"}

An example of a section loop:

{section name=customer loop=$custid}
id: {$custid[customer]}<br>
name: {$name[customer]|upper}<br>
{sectionelse}
No customer records found.<br>
{/section}

An example of a foreach loop:

{foreach from=$people item=person}
id: {$person.id}<br>
name: {$person.name|upper}<br>
{foreachelse}
No people records found.<br>
{/foreach}

</PRE>

{literal}
<script language="javascript">
    // javascript code will be taken literally
    // and not parsed by smarty
    function my_func() {
        alert("hello world");
    }
</script>
{/literal}

{include file="footer.tpl"}