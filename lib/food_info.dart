class FoodInfo {
  final String label;
  final String nama;
  final String kategori;
  final String statusHalal;
  final String asal;
  final String deskripsi;

  FoodInfo({
    required this.label,
    required this.nama,
    required this.kategori,
    required this.statusHalal,
    required this.asal,
    required this.deskripsi,
  });

  factory FoodInfo.fromJson(Map<String, dynamic> json) {
    return FoodInfo(
      label: json['label'],
      nama: json['nama'],
      kategori: json['kategori'],
      statusHalal: json['status_halal'],
      asal: json['asal'],
      deskripsi: json['deskripsi'],
    );
  }
}