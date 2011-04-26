#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_with	verbose		# verbose build (V=1)
#
%define		_rel		1
Summary:	Linux driver for WLAN cards based on rtl8192
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart bezprzewodowych opartych na układzie rtl8192
Name:		kernel%{_alt_kernel}-net-rtl8192
Version:	0003.0401.2011
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
# http://www.realtek.com/downloads/
Source0:	92ce_se_de_linux_mac80211_%{version}.tar.gz
# Source0-md5:	79fea598a4d7f20e3dac55273a0dd4f7
URL:		http://www.realtek.com/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
%{?with_dist_kernel:%requires_releq_kernel}
BuildRequires:	rpmbuild(macros) >= 1.379
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:Requires(postun):	kernel%{_alt_kernel}}
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Linux driver for WLAN cards based on rtl8192.

%description -l pl.UTF-8
Sterownik dla Linuksa do kart bezprzewodowych opartych na układzie
rtl8192.

%package firmware
Summary:	Firmware for WLAN cards based on rtl8192
Summary(pl.UTF-8):	Firmware do kart bezprzewodowych opartych na układzie rtl8192
Release:	%{_rel}
License:	Distributable
Group:		Base/Kernel

%description firmware
This is firmware for WLAN cards based on rtl8192.

%description firmware -l pl.UTF-8
Firmware do kart bezprzewodowych opartych na układzie rtl8192.

%prep
%setup -q -n rtl_92ce_92se_92de_linux_mac80211_%{version}

%build
%build_kernel_modules -m rtlwifi
%build_kernel_modules -m rtl8192ce -C rtl8192ce
%build_kernel_modules -m rtl8192de -C rtl8192de
%build_kernel_modules -m rtl8192se -C rtl8192se

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/firmware/rtlwifi

%install_kernel_modules -m rtlwifi -d kernel/drivers/net/wireless -s realtek
%install_kernel_modules -m rtl8192ce/rtl8192ce -d kernel/drivers/net/wireless -s realtek
%install_kernel_modules -m rtl8192de/rtl8192de -d kernel/drivers/net/wireless -s realtek
%install_kernel_modules -m rtl8192se/rtl8192se -d kernel/drivers/net/wireless -s realtek

cp -a firmware/rtlwifi/*.bin $RPM_BUILD_ROOT/lib/firmware/rtlwifi

# blacklist kernel module                                                           
cat > $RPM_BUILD_ROOT/etc/modprobe.d/%{_kernel_ver}/rtl8192.conf <<'EOF'
blacklist rtlwifi
blacklist rtl8192ce
blacklist rtl8192de
blacklist rtl8192se
alias rtlwifi rtlwifi-realtek
alias rtl8192ce rtl8192ce-realtek
alias rtl8192de rtl8192de-realtek
alias rtl8192se rtl8192se-realtek
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
%doc readme release_note
/etc/modprobe.d/%{_kernel_ver}/rtl8192.conf
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/*.ko*

%files firmware
%defattr(644,root,root,755)
%doc firmware/rtlwifi/Realtek-Firmware-License.txt
/lib/firmware/rtlwifi/*.bin
