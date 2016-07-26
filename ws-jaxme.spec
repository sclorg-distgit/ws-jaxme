%global pkg_name ws-jaxme
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%global base_name jaxme

Name:           %{?scl_prefix}%{pkg_name}
Version:        0.5.2
Release:        10.6%{?dist}
Epoch:          0
Summary:        Open source implementation of JAXB

License:        ASL 2.0
URL:            http://ws.apache.org/jaxme/
# svn export http://svn.apache.org/repos/asf/webservices/archive/jaxme/tags/R0_5_2/ ws-jaxme-0.5.2
# tar czf ws-jaxme-0.5.2-src.tar.gz ws-jaxme-0.5.2
Source0:        ws-jaxme-0.5.2-src.tar.gz
Source1:        ws-jaxme-bind-MANIFEST.MF
# generated docs with forrest-0.5.1
Patch0:         ws-jaxme-docs_xml.patch
Patch1:         ws-jaxme-catalog.patch
Patch2:         ws-jaxme-system-dtd.patch
Patch3:         ws-jaxme-jdk16.patch
Patch4:         ws-jaxme-ant-scripts.patch
Patch5:         ws-jaxme-use-commons-codec.patch
# Remove xmldb-api, deprecated since f17
Patch6:         ws-jaxme-remove-xmldb.patch
Patch7:         ws-jaxme-0.5.2-class-version15.patch
BuildArch:      noarch
BuildRequires:  %{?scl_prefix}javapackages-tools
BuildRequires:  %{?scl_prefix}ant >= 0:1.6
BuildRequires:  %{?scl_prefix}ant-apache-resolver
BuildRequires:  %{?scl_prefix}antlr-tool
BuildRequires:  %{?scl_prefix}apache-commons-codec
BuildRequires:  %{?scl_prefix}junit
BuildRequires:  hsqldb
BuildRequires:  %{?scl_prefix}log4j
BuildRequires:  %{?scl_prefix}xalan-j2
BuildRequires:  %{?scl_prefix}xerces-j2
BuildRequires:	docbook-style-xsl
BuildRequires:  docbook-dtds
BuildRequires:  zip
Requires:       %{?scl_prefix}antlr-tool
Requires:       %{?scl_prefix}apache-commons-codec
Requires:       %{?scl_prefix}junit
Requires:       hsqldb
Requires:       %{?scl_prefix}log4j
Requires:       %{?scl_prefix}xalan-j2
Requires:       %{?scl_prefix}xerces-j2

%description
A Java/XML binding compiler takes as input a schema 
description (in most cases an XML schema, but it may 
be a DTD, a RelaxNG schema, a Java class inspected 
via reflection, or a database schema). The output is 
a set of Java classes:
* A Java bean class matching the schema description. 
  (If the schema was obtained via Java reflection, 
  the original Java bean class.)
* Read a conforming XML document and convert it into 
  the equivalent Java bean.
* Vice versa, marshal the Java bean back into the 
  original XML document.

%package        javadoc
Summary:        Javadoc for %{pkg_name}

%description    javadoc
%{summary}.

%package        manual
Summary:        Documents for %{pkg_name}

%description    manual
%{summary}.

%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
for j in $(find . -name "*.jar"); do
    mv $j $j.no
done

%patch0 -p0
%patch1 -p0
%patch2 -p1
DOCBOOKX_DTD=`xmlcatalog %{_root_datadir}/sgml/docbook/xmlcatalog "-//OASIS//DTD DocBook XML V4.5//EN" 2>/dev/null`
%{__perl} -pi -e 's|@DOCBOOKX_DTD@|$DOCBOOKX_DTD|' src/documentation/manual/jaxme2.xml
%patch3 -p1
%patch4 -b .sav
%patch5 -b .sav
%patch6 -p1
%patch7 -p1
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
export CLASSPATH=$(build-classpath antlr commons-codec junit log4j xerces-j2 xalan-j2 xalan-j2-serializer):%{_root_datadir}/java/hsqldb.jar
ant all Docs.all \
-Dbuild.sysclasspath=first \
-Ddocbook.home=%{_root_datadir}/sgml/docbook \
-Ddocbookxsl.home=%{_root_datadir}/sgml/docbook/xsl-stylesheets

mkdir -p META-INF
cp -p %{SOURCE1} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u dist/jaxmeapi-%{version}.jar META-INF/MANIFEST.MF
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
install -dm 755 $RPM_BUILD_ROOT%{_javadir}/%{base_name}
for jar in dist/*.jar; do
   install -m 644 ${jar} $RPM_BUILD_ROOT%{_javadir}/%{base_name}/
done
(cd $RPM_BUILD_ROOT%{_javadir}/%{base_name} && 
    for jar in *-%{version}*; 
        do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; 
    done
)

(cd $RPM_BUILD_ROOT%{_javadir}/%{base_name} && 
    for jar in *.jar; 
        do ln -sf ${jar} ws-${jar}; 
    done
)

#javadoc
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr build/docs/src/documentation/content/apidocs \
    $RPM_BUILD_ROOT%{_javadocdir}/%{name}
rm -rf build/docs/src/documentation/content/apidocs

#manual
install -dm 755 $RPM_BUILD_ROOT%{_docdir}/%{pkg_name}-%{version}
cp -pr build/docs/src/documentation/content/* $RPM_BUILD_ROOT%{_docdir}/%{pkg_name}-%{version}
install -pm 644 LICENSE $RPM_BUILD_ROOT%{_docdir}/%{pkg_name}-%{version}
%{?scl:EOF}

%files
%doc LICENSE NOTICE
%{_javadir}/%{base_name}

%files javadoc
%doc LICENSE NOTICE
%doc %{_javadocdir}/%{name}

%files manual
%doc LICENSE NOTICE
%doc %{_docdir}/%{pkg_name}-%{version}

%changelog
* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:0.5.2-10.6
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:0.5.2-10.5
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:0.5.2-10.4
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:0.5.2-10.3
- Remove requires on java

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:0.5.2-10.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:0.5.2-10.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 00.5.2-10
- Mass rebuild 2013-12-27

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:0.5.2-9
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Tue Mar  5 2013 Hans de Goede <hdegoede@redhat.com> - 0:0.5.2-8
- Fix FTBFS (add xalan-j2-serializer to classpath) (rhbz#914580)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.5.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 23 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:0.5.2-6
- Add LICENSE and NOTICE files too all (sub)packages

* Fri Jul 27 2012 Hans de Goede <hdegoede@redhat.com> - 0:0.5.2-5
- Build all class files in 1.5 format (rhbz#842624)

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 6 2012 Alexander Kurtakov <akurtako@redhat.com> 0:0.5.2-3
- Fix the dependencies.

* Fri Apr 6 2012 Alexander Kurtakov <akurtako@redhat.com> 0:0.5.2-2
- Guideline fixes.

* Wed Feb 8 2012 Roland Grunberg <rgrunber@redhat.com> 0:0.5.2-1
- Update to 0.5.2.
- Remove xmldb-api due to deprecation.
- Fix ws-jaxme-ant-scripts.patch to apply cleanly.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.5.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Alexander Kurtakov <akurtako@redhat.com> 0:0.5.1-6
- Fix ant-nodeps in the classpath.

* Tue Dec 21 2010 Alexander Kurtakov <akurtako@redhat.com> 0:0.5.1-5
- Fix FTBFS.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.5.1-4.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.5.1-3.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 22 2008 Alexander Kurtakov <akurtako@redhat.com> - 0:0.5.1-2.3
- BR docbook-style-xsl.
- BR ant-apache-resolver.

* Wed Oct 22 2008 Alexander Kurtakov <akurtako@redhat.com> - 0:0.5.1-2.3
- Partial sync with jpackage to get build fixes.
- Add osgi manifest to jaxmeapi.jar.

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:0.5.1-2.2
- drop repotag
- fix license tag

* Mon Feb 12 2007 Deepak Bhole <dbhole@redhat.com> - 0:0.5.1-2jpp.1
- Update as per Fedora guidelines.

* Wed May 04 2006 Ralph Apel <r.apel at r-apel.de> - 0:0.5.1-1jpp
- First JPP-1.7 release

* Tue Dec 20 2005 Ralph Apel <r.apel at r-apel.de> - 0:0.5-1jpp
- Upgrade to 0.5

* Thu Sep 09 2004 Ralph Apel <r.apel at r-apel.de> - 0:0.3.1-1jpp
- Fix version in changelog
- Upgrade to 0.3.1

* Fri Aug 30 2004 Ralph Apel <r.apel at r-apel.de> - 0:2.0-0.b1.4jpp
- Build with ant-1.6.2

* Fri Aug 06 2004 Ralph Apel <r.apel at r-apel.de> - 0:2.0-0.b1.3jpp
- Void change

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 0:2.0-0.b1.2jpp
- Upgrade to Ant 1.6.X

* Fri Mar 04 2004 Ralph Apel <r.apel at r-apel.de> - 0:2.0-0.b1.1jpp
- First JPackage release
