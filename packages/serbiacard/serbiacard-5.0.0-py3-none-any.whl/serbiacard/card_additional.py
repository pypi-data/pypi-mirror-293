import ctypes


class SD_REGISTRATION_DATA(ctypes.Structure):
    _fields_ = [
        ("registrationData", ctypes.c_char * 4096),
        ("registrationDataSize", ctypes.c_long),
        ("signatureData", ctypes.c_char * 1024),
        ("signatureDataSize", ctypes.c_long),
        ("issuingAuthority", ctypes.c_char * 4096),
        ("issuingAuthoritySize", ctypes.c_long),
    ]


class SD_DOCUMENT_DATA(ctypes.Structure):
    _fields_ = [
        ("stateIssuing", ctypes.c_char * 50),
        ("stateIssuingSize", ctypes.c_long),
        ("competentAuthority", ctypes.c_char * 50),
        ("competentAuthoritySize", ctypes.c_long),
        ("authorityIssuing", ctypes.c_char * 50),
        ("authorityIssuingSize", ctypes.c_long),
        ("unambiguousNumber", ctypes.c_char * 30),
        ("unambiguousNumberSize", ctypes.c_long),
        ("issuingDate", ctypes.c_char * 16),
        ("issuingDateSize", ctypes.c_long),
        ("expiryDate", ctypes.c_char * 16),
        ("expiryDateSize", ctypes.c_long),
        ("serialNumber", ctypes.c_char * 20),
        ("serialNumberSize", ctypes.c_long),
    ]


class SD_VEHICLE_DATA(ctypes.Structure):
    _fields_ = [
        ("dateOfFirstRegistration", ctypes.c_char * 16),
        ("dateOfFirstRegistrationSize", ctypes.c_long),
        ("yearOfProduction", ctypes.c_char * 5),
        ("yearOfProductionSize", ctypes.c_long),
        ("vehicleMake", ctypes.c_char * 100),
        ("vehicleMakeSize", ctypes.c_long),
        ("vehicleType", ctypes.c_char * 100),
        ("vehicleTypeSize", ctypes.c_long),
        ("commercialDescription", ctypes.c_char * 100),
        ("commercialDescriptionSize", ctypes.c_long),
        ("vehicleIDNumber", ctypes.c_char * 100),
        ("vehicleIDNumberSize", ctypes.c_long),
        ("registrationNumberOfVehicle", ctypes.c_char * 20),
        ("registrationNumberOfVehicleSize", ctypes.c_long),
        ("maximumNetPower", ctypes.c_char * 20),
        ("maximumNetPowerSize", ctypes.c_long),
        ("engineCapacity", ctypes.c_char * 20),
        ("engineCapacitySize", ctypes.c_long),
        ("typeOfFuel", ctypes.c_char * 100),
        ("typeOfFuelSize", ctypes.c_long),
        ("powerWeightRatio", ctypes.c_char * 20),
        ("powerWeightRatioSize", ctypes.c_long),
        ("vehicleMass", ctypes.c_char * 20),
        ("vehicleMassSize", ctypes.c_long),
        ("maximumPermissibleLadenMass", ctypes.c_char * 20),
        ("maximumPermissibleLadenMassSize", ctypes.c_long),
        ("typeApprovalNumber", ctypes.c_char * 50),
        ("typeApprovalNumberSize", ctypes.c_long),
        ("numberOfSeats", ctypes.c_char * 20),
        ("numberOfSeatsSize", ctypes.c_long),
        ("numberOfStandingPlaces", ctypes.c_char * 20),
        ("numberOfStandingPlacesSize", ctypes.c_long),
        ("engineIDNumber", ctypes.c_char * 100),
        ("engineIDNumberSize", ctypes.c_long),
        ("numberOfAxles", ctypes.c_char * 20),
        ("numberOfAxlesSize", ctypes.c_long),
        ("vehicleCategory", ctypes.c_char * 50),
        ("vehicleCategorySize", ctypes.c_long),
        ("colourOfVehicle", ctypes.c_char * 50),
        ("colourOfVehicleSize", ctypes.c_long),
        ("restrictionToChangeOwner", ctypes.c_char * 200),
        ("restrictionToChangeOwnerSize", ctypes.c_long),
        ("vehicleLoad", ctypes.c_char * 20),
        ("vehicleLoadSize", ctypes.c_long),
    ]


class SD_PERSONAL_DATA(ctypes.Structure):
    _fields_ = [
        ("ownersPersonalNo", ctypes.c_char * 20),
        ("ownersPersonalNoSize", ctypes.c_long),
        ("ownersSurnameOrBusinessName", ctypes.c_char * 100),
        ("ownersSurnameOrBusinessNameSize", ctypes.c_long),
        ("ownerName", ctypes.c_char * 100),
        ("ownerNameSize", ctypes.c_long),
        ("ownerAddress", ctypes.c_char * 200),
        ("ownerAddressSize", ctypes.c_long),
        ("usersPersonalNo", ctypes.c_char * 20),
        ("usersPersonalNoSize", ctypes.c_long),
        ("usersSurnameOrBusinessName", ctypes.c_char * 100),
        ("usersSurnameOrBusinessNameSize", ctypes.c_long),
        ("usersName", ctypes.c_char * 100),
        ("usersNameSize", ctypes.c_long),
        ("usersAddress", ctypes.c_char * 200),
        ("usersAddressSize", ctypes.c_long),
    ]


class EID_DOCUMENT_DATA(ctypes.Structure):
    _fields_ = [
        ("docRegNo", ctypes.c_char * 9),
        ("docRegNoSize", ctypes.c_int),
        ("documentType", ctypes.c_char * 2),
        ("documentTypeSize", ctypes.c_int),
        ("issuingDate", ctypes.c_char * 10),
        ("issuingDateSize", ctypes.c_int),
        ("expiryDate", ctypes.c_char * 10),
        ("expiryDateSize", ctypes.c_int),
        ("issuingAuthority", ctypes.c_char * 100),
        ("issuingAuthoritySize", ctypes.c_int),
        ("documentSerialNumber", ctypes.c_char * 10),
        ("documentSerialNumberSize", ctypes.c_int),
        ("chipSerialNumber", ctypes.c_char * 14),
        ("chipSerialNumberSize", ctypes.c_int),
    ]


class EID_FIXED_PERSONAL_DATA(ctypes.Structure):
    _fields_ = [
        ("personalNumber", ctypes.c_char * 13),
        ("personalNumberSize", ctypes.c_int),
        ("surname", ctypes.c_char * 200),
        ("surnameSize", ctypes.c_int),
        ("givenName", ctypes.c_char * 200),
        ("givenNameSize", ctypes.c_int),
        ("parentGivenName", ctypes.c_char * 200),
        ("parentGivenNameSize", ctypes.c_int),
        ("sex", ctypes.c_char * 2),
        ("sexSize", ctypes.c_int),
        ("placeOfBirth", ctypes.c_char * 200),
        ("placeOfBirthSize", ctypes.c_int),
        ("stateOfBirth", ctypes.c_char * 200),
        ("stateOfBirthSize", ctypes.c_int),
        ("dateOfBirth", ctypes.c_char * 10),
        ("dateOfBirthSize", ctypes.c_int),
        ("communityOfBirth", ctypes.c_char * 200),
        ("communityOfBirthSize", ctypes.c_int),
        ("statusOfForeigner", ctypes.c_char * 200),
        ("statusOfForeignerSize", ctypes.c_int),
        ("nationalityFull", ctypes.c_char * 200),
        ("nationalityFullSize", ctypes.c_int),
    ]


class EID_VARIABLE_PERSONAL_DATA(ctypes.Structure):
    _fields_ = [
        ("state", ctypes.c_char * 100),
        ("stateSize", ctypes.c_int),
        ("community", ctypes.c_char * 200),
        ("communitySize", ctypes.c_int),
        ("place", ctypes.c_char * 200),
        ("placeSize", ctypes.c_int),
        ("street", ctypes.c_char * 200),
        ("streetSize", ctypes.c_int),
        ("houseNumber", ctypes.c_char * 20),
        ("houseNumberSize", ctypes.c_int),
        ("houseLetter", ctypes.c_char * 8),
        ("houseLetterSize", ctypes.c_int),
        ("entrance", ctypes.c_char * 10),
        ("entranceSize", ctypes.c_int),
        ("floor", ctypes.c_char * 6),
        ("floorSize", ctypes.c_int),
        ("apartmentNumber", ctypes.c_char * 12),
        ("apartmentNumberSize", ctypes.c_int),
        ("addressDate", ctypes.c_char * 10),
        ("addressDateSize", ctypes.c_int),
        ("addressLabel", ctypes.c_char * 60),
        ("addressLabelSize", ctypes.c_int),
    ]


class EID_PORTRAIT(ctypes.Structure):
    _fields_ = [("portrait", ctypes.c_byte * 7700), ("portraitSize", ctypes.c_int)]


class EID_CERTIFICATE(ctypes.Structure):
    _fields_ = [("certificate", ctypes.c_byte * 2048), ("certificateSize", ctypes.c_int)]
