//===----------------------------------------------------------------------===//
// This file is automatically generated by scripts/generate_serialization.py
// Do not edit this file manually, your changes will be overwritten
//===----------------------------------------------------------------------===//

#include "duckdb/common/serializer/serializer.hpp"
#include "duckdb/common/serializer/deserializer.hpp"
#include "duckdb/parser/parsed_data/extra_drop_info.hpp"

namespace duckdb {

void ExtraDropInfo::Serialize(Serializer &serializer) const {
	serializer.WriteProperty<ExtraDropInfoType>(100, "info_type", info_type);
}

unique_ptr<ExtraDropInfo> ExtraDropInfo::Deserialize(Deserializer &deserializer) {
	auto info_type = deserializer.ReadProperty<ExtraDropInfoType>(100, "info_type");
	unique_ptr<ExtraDropInfo> result;
	switch (info_type) {
	case ExtraDropInfoType::SECRET_INFO:
		result = ExtraDropSecretInfo::Deserialize(deserializer);
		break;
	default:
		throw SerializationException("Unsupported type for deserialization of ExtraDropInfo!");
	}
	return result;
}

void ExtraDropSecretInfo::Serialize(Serializer &serializer) const {
	ExtraDropInfo::Serialize(serializer);
	serializer.WriteProperty<SecretPersistType>(200, "persist_mode", persist_mode);
	serializer.WritePropertyWithDefault<string>(201, "secret_storage", secret_storage);
}

unique_ptr<ExtraDropInfo> ExtraDropSecretInfo::Deserialize(Deserializer &deserializer) {
	auto result = duckdb::unique_ptr<ExtraDropSecretInfo>(new ExtraDropSecretInfo());
	deserializer.ReadProperty<SecretPersistType>(200, "persist_mode", result->persist_mode);
	deserializer.ReadPropertyWithDefault<string>(201, "secret_storage", result->secret_storage);
	return std::move(result);
}

} // namespace duckdb
