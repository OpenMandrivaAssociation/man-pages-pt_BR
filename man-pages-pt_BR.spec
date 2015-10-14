%define LNG pt_BR

Summary:	Brazilian man (manual) pages from the Linux Documentation Project
Name:		man-pages-%{LNG}
Version:	0.1
Release:	21
License:	GPLv2
Group:		System/Internationalization
Url:		http://br.tldp.org/projetos/man/man.html
# the tarball has to build, files got from the web with wget.
# files dated 2002-11-21 -- pablo
Source0:	http://br.tldp.org/projetos/man/arquivos/man-pages-pt_BR.tar.bz2
#Icon:	books-%{LNG}.xpm
BuildArch:	noarch
BuildRequires:	man
Requires:	locales-pt
Requires:	man
Autoreqprov:	false
Conflicts:	filesystem < 3.0-17

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
mkdir -p %{buildroot}/%{_mandir}/%{LNG}/man{1,2,3,4,5,6,7,8}

for i in 1 2 3 4 5 6 7 8 ; do
	cp -adpvrf man$i %{buildroot}/%{_mandir}/%{LNG}/||:
done

LANG=%{LNG} DESTDIR=%{buildroot} %{_bindir}/mandb %{buildroot}/%{_mandir}/%{LNG}

mkdir -p %{buildroot}%{_sysconfdir}/cron.weekly
cat > %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%{LNG}.cron << EOF
#!/bin/bash
LANG=%{LNG} %{_bindir}/mandb %{_mandir}/%{LNG}
exit 0
EOF
chmod a+x %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%{LNG}.cron

mkdir -p  %{buildroot}/var/cache/man/%{LNG}

touch %{buildroot}/var/cache/man/%{LNG}/whatis

%post
%create_ghostfile /var/cache/man/%{LNG}/whatis root root 644

%files
%dir /var/cache/man/%{LNG}
%ghost %config(noreplace) /var/cache/man/%{LNG}/whatis
%{_mandir}/%{LNG}/man*
%{_mandir}/%{LNG}/cat*
%{_mandir}/%{LNG}/index.db*
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/cron.weekly/makewhatis-%{LNG}.cron
