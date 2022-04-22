#
# Conditonal build:
%bcond_without	nautilus	# Nautilus plugin

Summary:	Minimal terminal for GNOME
Summary(pl.UTF-8):	Minimalny terminal dla GNOME
Name:		gnome-console
Version:	42
%define	subver	beta
Release:	0.%{subver}.1
License:	GPL v3+
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/gnome-console/42/%{name}-%{version}.%{subver}.tar.xz
# Source0-md5:	43b2ab69babd8222a2786a27a0aa1b88
Patch0:		%{name}-no-update.patch
URL:		https://gitlab.gnome.org/GNOME/console
# -std=c17
BuildRequires:	gcc >= 6:7
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.66
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	gtk+3-devel >= 3.24
BuildRequires:	libgtop-devel >= 2.0
BuildRequires:	libhandy1-devel >= 1.5
BuildRequires:	libsass-devel
# -std=gnu++17
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	meson >= 0.59.0
%{?with_nautilus:BuildRequires:	nautilus-devel >= 3.0}
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	sassc
BuildRequires:	tar >= 1:1.22
BuildRequires:	vte-devel >= 0.67
BuildRequires:	xz
Requires(post,postun):	gtk-update-icon-cache
Requires:	glib2 >= 1:2.66
Requires:	gsettings-desktop-schemas
Requires:	gtk+3 >= 3.24
Requires:	hicolor-icon-theme
Requires:	libhandy1 >= 1.5
Requires:	vte >= 0.67
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Console is supposed to be a simple terminal emulator for the average
user to carry out simple CLI tasks and aims to be a "core" app for
GNOME/Phosh.

%description -l pl.UTF-8
Console ma być prostym emulatorem terminala dla przeciętnego
użytkownika, pozwalającym na wykonywanie prostych zadań w wierszu
poleceń, "podstawową" aplikacją dla GNOME/Phosh.

%package -n nautilus-extension-console
Summary:	Console plugin for Nautilus
Summary(pl.UTF-8):	Wtyczka terminala dla Nautilusa
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	nautilus >= 3.0

%description -n nautilus-extension-console
Console plugin for Nautilus.

%description -n nautilus-extension-console -l pl.UTF-8
Wtyczka terminala dla Nautilusa.

%prep
%setup -q -n %{name}-%{version}.%{subver}
%patch0 -p1

%build
%meson build \
	%{!?with_nautilus:-Dnautilus=disabled}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

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

%if %{with nautilus}
%files -n nautilus-extension-console
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nautilus/extensions-3.0/libkgx-nautilus.so
%endif
