%define LANG pt_BR

Summary:	Brazilian man (manual) pages from the Linux Documentation Project.
Name:		man-pages-%LANG
Version:	0.1
Release:	1mdk
License:	GPL
Group:	System/Internationalization
URL: 	http://br.tldp.org/projetos/man/man.html
# the tarball has to build, files got from the web with wget.
# files dated 2002-11-21 -- pablo
Source:	http://br.tldp.org/projetos/man/arquivos/man-pages-pt_BR.tar.bz2
#Icon:		books-%LANG.xpm
Buildroot: %_tmppath/%name-root
BuildRequires: man => 1.5j-8mdk
Requires: locales-pt, man => 1.5j-8mdk
Prereq: sed grep man
Autoreqprov: false
BuildArchitectures: noarch
Obsoletes: man-%LANG, manpages-%LANG
Provides: man-%LANG, manpages-%LANG

%description
A large collection of man pages (reference material) from the Linux 
Documentation Project (LDP), translated to Brzailian Portuguese.
The man pages are organized into the following sections:

        Section 1:  User commands (intro only)
        Section 2:  System calls
        Section 3:  Libc calls
        Section 4:  Devices (e.g., hd, sd)
        Section 5:  File formats and protocols (e.g., wtmp, /etc/passwd, nfs)
        Section 5:  Games (intro only)
        Section 7:  Conventions, macro packages, etc. (e.g., nroff, ascii)
        Section 8:  System administration (intro only)
        Section 9:  Kernel routines

%define _mandir2 /usr/X11R6/man

%prep
%setup -n man-pages-pt_BR

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%_mandir/%LANG/man{1,2,3,4,5,6,7,8}
mkdir -p $RPM_BUILD_ROOT/var/catman/%LANG/cat{1,2,3,4,5,6,7,8,9,n}

for i in 1 2 3 4 5 6 7 8 ; do
	cp -adpvrf man$i $RPM_BUILD_ROOT/%_mandir/%LANG/||:
done

LANG=%LANG DESTDIR=$RPM_BUILD_ROOT %_sbindir/makewhatis $RPM_BUILD_ROOT/%_mandir/%LANG

mkdir -p $RPM_BUILD_ROOT/etc/cron.weekly
cat > $RPM_BUILD_ROOT/etc/cron.weekly/makewhatis-%LANG.cron << EOF
#!/bin/bash
LANG=%LANG %_sbindir/makewhatis %_mandir/%LANG
exit 0
EOF
chmod a+x $RPM_BUILD_ROOT/etc/cron.weekly/makewhatis-%LANG.cron

mkdir -p  $RPM_BUILD_ROOT/var/cache/man/%LANG


%postun
# 0 means deleting the package
if [ "$1" = "0" ]; then
   ## Force removing of /var/catman/%LANG, if there isn't any man page
   ## directory /%_mandir/%LANG
   if [ ! -d %_mandir/%LANG ] ; then
       rm -rf /var/catman/%LANG
   fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,man,755)
%dir %_mandir/%LANG
%dir /var/cache/man/%LANG
%verify(not md5 mtime size) /var/cache/man/%LANG/whatis
%_mandir/%LANG/man*
#%dir %_mandir2/%LANG
#%_mandir2/%LANG/man*
%attr(755,root,man)/var/catman/%LANG
%config(noreplace) %attr(755,root,root)/etc/cron.weekly/makewhatis-%LANG.cron

