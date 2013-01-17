%define LNG pt_BR
%define name man-pages-%LNG
%define version 0.1
%define release %mkrel 11

Summary:	Brazilian man (manual) pages from the Linux Documentation Project
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:	System/Internationalization
URL: 	http://br.tldp.org/projetos/man/man.html
# the tarball has to build, files got from the web with wget.
# files dated 2002-11-21 -- pablo
Source:	http://br.tldp.org/projetos/man/arquivos/man-pages-pt_BR.tar.bz2
#Icon:		books-%LNG.xpm
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: man => 1.5j-8mdk
Requires: locales-pt, man => 1.5j-8mdk
Autoreqprov: false
BuildArchitectures: noarch

%description
A large collection of man pages (reference material) from the Linux 
Documentation Project (LDP), translated to Brzailian Portuguese.
The man pages are organized into the following sections:

        Section 1:  User commands (intro only)
        Section 2:  System calls
        Section 3:  Libc calls
        Section 4:  Devices (e.g., hd, sd)
        Section 5:  File formats and protocols (e.g., wtmp, %{_sysconfdir}passwd, nfs)
        Section 5:  Games (intro only)
        Section 7:  Conventions, macro packages, etc. (e.g., nroff, ascii)
        Section 8:  System administration (intro only)
        Section 9:  Kernel routines

%prep
%setup -n man-pages-pt_BR

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%_mandir/%LNG/man{1,2,3,4,5,6,7,8}

for i in 1 2 3 4 5 6 7 8 ; do
	cp -adpvrf man$i %{buildroot}/%_mandir/%LNG/||:
done

LANG=%LNG DESTDIR=%{buildroot} %{_bindir}/mandb %{buildroot}/%_mandir/%LNG

mkdir -p %{buildroot}%{_sysconfdir}/cron.weekly
cat > %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron << EOF
#!/bin/bash
LANG=%LNG %{_bindir}/mandb %_mandir/%LNG
exit 0
EOF
chmod a+x %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron

mkdir -p  %{buildroot}/var/cache/man/%LNG

touch %{buildroot}/var/cache/man/%LNG/whatis

%post
%create_ghostfile /var/cache/man/%LNG/whatis root root 644

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,man,755)
%dir %_mandir/%LNG
%dir /var/cache/man/%LNG
%ghost %config(noreplace) /var/cache/man/%LNG/whatis
%_mandir/%LNG/man*
%{_mandir{/%{LNG}/cat*
%{_mandir}/%{LNG}/CACHEDIR.TAG*
%{_mandir}/%{LNG}/index.db*
#%_mandir/%LNG/whatis
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1-10mdv2011.0
+ Revision: 666375
- mass rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1-9mdv2011.0
+ Revision: 609326
- rebuild
- fix build
- fix typos
- fix build
- rebuild
- rebuilt for 2010.1

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0.1-6mdv2009.1
+ Revision: 351583
- rebuild

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 0.1-5mdv2009.0
+ Revision: 223193
- rebuild

* Tue Jan 15 2008 Thierry Vignaud <tv@mandriva.org> 0.1-4mdv2008.1
+ Revision: 152990
- rebuild
- rebuild
- kill re-definition of %%buildroot on Pixel's request
- fix summary-ended-with-dot

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu May 31 2007 Adam Williamson <awilliamson@mandriva.org> 0.1-2mdv2008.0
+ Revision: 33477
- rebuild for new era; drop /var/catman (wildly obsolete)


* Wed Jul 23 2003 Pablo Saratxaga <pablo@mandrakesoft.com> 0.1-1mdk
- first package

