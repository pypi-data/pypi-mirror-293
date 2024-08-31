<?xml version="1.0" encoding="UTF-8"?>
<!--
Namn:		ERMS-SVK-ARENDE.sch
Version:	0.1
Ändrad:		2023-09-05
Ändrad av:	Henrik Vitalis
-->

<!-- Inklusive Svenska kyrkans anpassningar -->
<!-- E-ARK ERMS Schematron rules version 2.1 -->
<!-- E-ARK ERMS Schematron rules version 1.0 -->
<!-- <ns uri="https://DILCIS.eu/XML/ERMS" prefix="erms"/> -->

<schema xmlns="http://purl.oclc.org/dsdl/schematron"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" queryBinding="xslt3">
	<ns uri="http://www.w3.org/2005/xpath-functions" prefix="fn"/>
    <ns uri="http://www.loc.gov/mads/rdf/v1#" prefix="madsrdf"/>
	<ns uri="https://DILCIS.eu/XML/ERMS" prefix="erms"/>
    <ns uri="https://xml.svenskakyrkan.se/ERMS-SVK-ARENDE" prefix="svk"/>
    <ns uri="https://xml.svenskakyrkan.se/ERMS-SVK-ARENDE-element" prefix="elm"/>

<!-- Regler för Svenska kyrkans anpassning av ERMS -->

	<pattern id="svk_rules">
		<rule context="//erms:control">
			<!-- ERMS-SVK:1-2 -->
			<assert test="count(erms:identification[@identificationType='arkivbildare'])=1">Det måste finnas en Identifikator av typen "arkivbildare" (ERMS-SVK:1-2).</assert>
			<assert test="count(erms:identification[@identificationType='ärendenummer'])=1">Det måste finnas en Identifikator av typen "ärendenummer" (ERMS-SVK:1-2).</assert>
			<assert test="count(erms:identification[@identificationType='organisationsnummer'])=1 or count(erms:identification[@identificationType='aid'])=1">
				Det måste finnas en Identifikator av typen "organisationsnummer" eller "aid" (ERMS-SVK:1-2).</assert>
			<assert test="matches(erms:identification[@identificationType='organisationsnummer'], '[0-9]{10}')">Organisationsnummer måste skrivas med 10 siffror utan bindestreck.</assert>
		</rule>
		<rule context="erms:control/erms:classificationSchema/erms:textualDescriptionOfClassificationSchema/erms:p">
		    <!-- ERMS-SVK:4 -->
		    <assert test=".='KlaSL2016_1.0' or .='KlaSN2018_1.0' or .='KlaSS2016_1.0'">Klassificeringsstruktur måste väljas från SVK-VÄRDELISTA 2 (ERMS-SVK:4).</assert>
		</rule>

		<rule context="erms:control/erms:maintenanceInformation/erms:maintenanceAgency">
			<!-- ERMS-SVK:10 -->
			<assert test="erms:agencyCode/@type = ('aid', 'organisationsnummer')">Endast aid och organisationnummer är giltiga värden</assert>
		</rule>

		<rule context="erms:control/erms:maintenanceInformation/erms:maintenanceAgency/erms:agencyCode[@type='organisationsnummer']">
			<assert test="fn:matches(., '[0-9]{10}')">Organisationsnummer måste skrivas med 10 siffror utan bindestreck.</assert>
		</rule>





		<rule context="//erms:aggregations">
		    <!-- ERMS-SVK:22 -->
		    <assert test="count(*)=1">XML-filen får inte innehålla mer än en ärendeakt (ERMS-SVK:22).</assert>
		</rule>
		<rule context="//erms:aggregation">
		    <!-- ERMS-SVK:24 -->
		    <assert test="@aggregationType='caseFile'">Typen av aggregation ska alltid vara "caseFile" (ERMS-SVK:24).</assert>
			<!-- ERMS-SVK:26 -->

			<assert test="count(.//erms:extraId[@extraIdType='organisationsnummer'])=1 or count(.//erms:extraId[@extraIdType='aid'])=1">
				Arkivansvarigs ID är obligatoriskt. Värdet för extraIdType måste väljas från SVK-VÄRDELISTA 4 (ERMS-SVK:26).</assert>
		</rule>
		<rule context="//erms:aggregation/erms:objectId">
		    <!-- ERMS-SVK:25 -->
			<assert test="fn:matches(., '[A-Ö]+ \d{4}-\d{4}')">Ärendenumret ska ha formatet [diariekod] [årtal]-[löpnummer]. Löpnumret ska bestå av fyra siffror och fylls vid behov ut med nollor (ERMS-SVK:25).</assert>
		</rule>
		<rule context="//erms:aggregation/erms:extraId[@extraIdType='organisationsnummer']">
				<assert test="fn:matches(., '[0-9]{10}')">Organisationsnummer måste skrivas med 10 siffror utan bindestreck.</assert>
		</rule>

		<!-- Nedanstående funkar inte -->
		<!--
		<rule context="//erms:aggregation/erms:extraId">
		    ERMS-SVK:27
			<assert test="@extraIdType = 'deliveringSystemId'">Om elementet Intern identifikator används, måste attributet extraIdType ha värdet 'deliveringSystemId' (ERMS-SVK:27).</assert>
		</rule>
		Ovanstående funkar inte
		-->

		<rule context= "//erms:aggregation/erms:otherTitle">
		    <!-- ERMS-SVK:35 -->
			<!-- Ev. lägga till regel om att otherTitle bara får förekomma en gång -->
			<assert test="@titleType = 'public'">Om elementet otherTitle används, måste attributet titleType ha värdet 'public' (ERMS-SVK:35).</assert>
		</rule>

		<rule context="//erms:aggregation/erms:status">
		    <!-- ERMS-SVK:36 -->
			<assert test="@value = 'closed' or @value = 'obliterated'">Ärendestatus får enbart ha något av värdena 'closed' eller 'obliterated' (ERMS-SVK:36).</assert>
		</rule>

		<rule context="//erms:aggregation/erms:relation">
		    <!-- ERMS-SVK:37 -->
		    <assert test="@relationType = 'reference'">Om elementet Ärendereferens används, måste attributet relationTyp ha värdet 'reference' (ERMS-SVK:37).</assert>
		</rule>

		<rule context="//erms:aggregation/erms:restriction">
		    <!-- ERMS-SVK36 -->
			<assert test="@restrictionType = 'confidential'">Om elementet Sekretess används, måste attributet restrictionType ha värdet 'confidential' (ERMS-SVK36).</assert>
		</rule>

		<rule context="//erms:aggregation/erms:restriction/erms:dates">
		    <!-- ERMS-SVK38 -->
			<assert test="count(erms:date) = 1">Endast ett datum, Sekretessdatum, är tillåtet (ERMS-SVK38).</assert>
			 <!-- ERMS-SVK39 -->
			<assert test="erms:date/@dateType='created'">Om elementet Sekretessdatum används, måste attributet dateType ha värdet 'created' (ERMS-SVK38).</assert>
		</rule>

		<rule context="//erms:aggregation/erms:agents">
		    <!-- ERMS SVK41-46 -->
		    <assert test="count(erms:agent[@agentType='creator'])&lt;2">Aktör av typen "creator" får bara förekomma en gång.</assert>
		    <assert test="count(erms:agent[@agentType='responsible_person'])&lt;2">Aktör av typen "responsible_person" får bara förekomma en gång.</assert>
		    <assert test="count(erms:agent[@otherAgentType='closing_person'])&lt;2">Aktör av typen "closing_person" får bara finnas en gång.</assert>
		</rule>

		<rule context="//erms:aggregation/erms:agents/erms:agent">
		    <assert test="@agentType=('creator', 'responsible_person', 'editor', 'counterpart', 'other')">Aktörer måste välja från värdelista</assert>
			<assert test="@otherAgentType='closing_person' or fn:empty(@otherAgentType)">Om attributet otherAgentType använd, måste värdet vara "closing_person"</assert>
		</rule>

		<rule context="//erms:aggregation/erms:dates">
		    <!-- ERMS SVK49-51 -->
		    <assert test="count(erms:date[@dateType='created'])&lt;2">Datum av typen "created" får bara finnas en gång.</assert>
		    <assert test="count(erms:date[@dateType='opened'])=1">Datum av typen "opened" är obligatoriskt och får bara finnas en gång.</assert>
		    <assert test="count(erms:date[@dateType='closed'])=1">Datum av typen "closed" är obligatoriskt och får bara finnas en gång.</assert>
		</rule>

		<rule context="//erms:aggregation/erms:dates/erms:date">
			<assert test="@dateType=('created', 'opened', 'closed')">Datum man bara vara av typen "create", "opened" eller "closed".</assert>
		</rule>

		<rule context="//erms:aggregation/erms:action">
		    <!-- ERMS-SVK53-56 -->
		    <assert test="erms:actionType='beslut'">Elementet actionType måste ha värdet "beslut"</assert>
		    <assert test="count(erms:dates/erms:actionDate)&lt;2">Elementet actionDate får bara förekomma en gång.</assert>
		    <assert test="erms:dates/erms:actionDate/@dateType='decision_date'">Attributet dateType måste ha värdet "decision_date"</assert>
		    <assert test="count(erms:agents/erms:agent)&lt;2">Elementet agent får bara förekomma en gång.</assert>
		    <assert test="erms:agents/erms:agent/@agentType='authorising_person'">Attributet agentType måste ha värdet "authorising_person"</assert>
		</rule>

		<rule context="//erms:aggregation/erms:notes">
            <!-- ERMS-SVK57-58 -->
            <assert test="count(erms:note)&lt;2">Elementet note får bara förekomma en gång.</assert>
            <assert test="erms:note/@noteType='comment'">Attributet noteType måste ha värdet "comment".</assert>
        </rule>

		<rule context="//erms:record">
            <!-- ERMS-SVK84 -->
            <assert test="@recordType=('ärendedokument', 'avtalsdokument')">Attributet recordType måste vara "ärendedokument" eller "avtalsdokument"</assert>
			<!-- Här måste läggas in element som är oblgatoriska i erms-svk men inte i erms-standard -->
			<assert test="count(erms:status)=1">Elementet status är obligatoriskt och får bara förekomma en gång.</assert>
			<assert test="erms:direction/@otherDirectionDefinition='internal'">internal</assert>
        </rule>

		<rule context="//erms:record/erms:objectId">
		    <!-- ERMS-SVK86 -->
			<assert test="matches(., '[A-Ö]+ \d{4}-\d{4}:[1-9][0-9]*')">Dokumentnumret ska ha formatet [diariekod] [årtal]-[löpnummer]:[löpnummer]. (ERMS-SVK86).</assert>
		</rule>

		<rule context="//erms:record/erms:extraId">
		    <!-- ERMS-SVK87 -->
			<assert test="count(../erms:extraId)&lt;2">Elementet extraId får bara förekomma en gång.</assert>
			<assert test="@extraIdType = 'deliveringSystemId'">Om elementet Intern identifikator används, måste attributet extraIdType ha värdet 'deliveringSystemId' (ERMS-SVK87).</assert>
		</rule>

		<rule context= "//erms:record/erms:otherTitle">
		    <!-- ERMS-SVK94 -->
			<!-- Ev. lägga till regel om att otherTitle bara får förekomma en gång -->
			<assert test="@titleType = 'public'">Om elementet Annan titel används, måste attributet titleType ha värdet 'public' (ERMS-SVK94).</assert>
		</rule>

		<rule context="//erms:record/erms:status">
		    <!-- ERMS-SVK95 -->
			<assert test="@value = ('closed', 'obliterated')">Handlingens status får enbart ha något av värdena 'closed' eller 'obliterated' (ERMS-SVK95).</assert>
		</rule>
		<rule context="//erms:record/erms:relation">
		    <!-- ERMS-SVK97 -->
		    <assert test="@relationType = 'reference'">Om elementet Dokumentreferens används, måste attributet relationType ha värdet 'reference' (ERMS-SVK97).</assert>
		</rule>

		<rule context="//erms:record/erms:restriction">
		    <!-- ERMS-SVK98 -->
		    <assert test="@restrictionType = 'confidential'">Om elementet Sekretess används, måste attributet restrictionType ha värdet 'confidential' (ERMS-SVK98).</assert>
		</rule>

		<rule context="//erms:record/erms:restriction/erms:dates/erms:date">
			<!-- ERMS-SVK101 -->
			<assert test="@dateType = 'created'">Om elementet Sekretessdatum används måste attributet dateType ha värdet 'created' (ERMS-SVK101).</assert>
		</rule>

		<rule context="//erms:record/erms:direction">
			<!-- ERMS-SVK102 -->
			<assert test="@directionDefinition = ('incoming', 'outgoing', 'other')">Attributert directionDefinition måste ha värdet 'incoming, 'outgoing' eller 'other' (ERMS-SVK102).</assert>
		</rule>

		<rule context="//erms:record/erms:agents">
		    <!-- ERMS SVK103-108 -->
		    <assert test="count(erms:agent[@agentType='creator'])&lt;2">Aktör av typen Skapare får bara förekomma en gång (ERMS_SVK104).</assert>
		    <assert test="count(erms:agent[@agentType='responsible_person'])&lt;2">Aktör av typen Ansvarig får bara förekomma en gång.</assert>
		</rule>



	</pattern>

	</schema>
