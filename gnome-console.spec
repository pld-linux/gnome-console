# TODO: switch to gtk4-update-icon-cache
Summary:	Minimal terminal for GNOME
Summary(pl.UTF-8):	Minimalny terminal dla GNOME
Name:		gnome-console
Version:	48.1
Release:	1
License:	GPL v3+
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/gnome-console/48/%{name}-%{version}.tar.xz
# Source0-md5:	d89577de3b5b6cd648314806816383d4
Patch0:		%{name}-no-update.patch
URL:		https://apps.gnome.org/Console/
# -std=c17
BuildRequires:	gcc >= 6:7
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.80
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	gtk4-devel >= 4.14
BuildRequires:	libadwaita-devel >= 1.6
BuildRequires:	libgtop-devel >= 2.0
BuildRequires:	meson >= 0.59.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pango-devel >= 1:1.51.2
BuildRequires:	pcre2-8-devel >= 10.32
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	tar >= 1:1.22
BuildRequires:	vte-gtk4-devel >= 0.77.0
BuildRequires:	xz
Requires(post,postun):	gtk-update-icon-cache
Requires:	glib2 >= 1:2.80
Requires:	gsettings-desktop-schemas
Requires:	gtk4 >= 4.14
Requires:	hicolor-icon-theme
Requires:	libadwaita >= 1.6
Requires:	pango >= 1:1.51.2
Requires:	vte-gtk4 >= 0.77.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Console is supposed to be a simple terminal emulator for the average
user to carry out simple CLI tasks and aims to be a "core" app for
GNOME/Phosh.

%description -l pl.UTF-8
Console ma być prostym emulatorem terminala dla przeciętnego
użytkownika, pozwalającym na wykonywanie prostych zadań w wierszu
poleceń, "podstawową" aplikacją dla GNOME/Phosh.

%prep
%setup -q
%patch -P0 -p1

%build
%meson

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

# not supported by glibc (as of 2.37)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang kgx

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas
%update_icon_cache hicolor

%postun
%glib_compile_schemas
%update_icon_cache hicolor

%files -f kgx.lang
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_bindir}/kgx
%{_datadir}/dbus-1/services/org.gnome.Console.service
%{_datadir}/glib-2.0/schemas/org.gnome.Console.gschema.xml
%{_datadir}/metainfo/org.gnome.Console.metainfo.xml
%{_desktopdir}/org.gnome.Console.desktop
%{_iconsdir}/hicolor/scalable/apps/org.gnome.Console.svg
%{_iconsdir}/hicolor/symbolic/apps/org.gnome.Console-symbolic.svg
