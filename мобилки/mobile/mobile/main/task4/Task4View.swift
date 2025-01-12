//
//  Task4View.swift
//  mobile
//

import SwiftUI

struct Task4View: View {
    // камера
    @State private var cameraOpen = false
    @State private var freshPhoto = false
    @State private var image: UIImage? = nil
    @State private var newTemp: tempPhoto? = nil
    @State private var newMeta: MetaPhoto? = nil
    @State private var photoTrigger = false
    
    // данные
    @StateObject private var photoLoader = PhotoLoader()
    @State private var selectedMetaPhoto: MetaPhoto? = nil
    @State private var showingDetails: Bool = false
    @State private var selectedTags: [Bool] = []
    
    // поиск
    @State private var srchName = ""
    @State private var srchDesc = ""
    @State private var srchTag: Int? = nil
    
    private var cols: [GridItem] = [
        GridItem(.flexible()),
        GridItem(.flexible()),
        GridItem(.flexible())
    ]
    
    var body: some View {
        NavigationStack {
            HStack{
                Spacer()
                Text("Галерея")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                
                Spacer()
                
                Button {
                    cameraOpen = true
                } label: {
                    Image(systemName: "camera")
                        .imageScale(.large)
                }
            }
            .padding(.horizontal)
            List {
                TextField("Поиск по имени", text: $srchName)
                TextField("Поиск по описанию", text: $srchDesc)
                Picker(selection: $srchTag) {
                    Text("Не выбрано").tag(Optional<Int>(nil))
                    ForEach(photoLoader.TagList) { atag in
                        Text("\(atag.Name)").tag(Optional(atag.id))
                    }
                } label: {
                    Text("Тег")
                }

                HStack {
                    Button {
                        photoLoader.filterCollection(srchName: srchName, srchDesc: srchDesc, srchTag: srchTag)
                    } label: {
                        Text("Поиск")
                    }
                    .buttonStyle(.borderless)
                    .padding()
                    
                    Button {
                        srchName = ""
                        srchDesc = ""
                        srchTag = nil
                        photoLoader.resetFiltering()
                    } label: {
                        Text("Очистить")
                    }
                    .buttonStyle(.borderless)
                    .padding()
                }
            }
            ScrollView {
                LazyVGrid(
                    columns: cols,
                    alignment: .center,
                    spacing: 20
                ) {
                    ForEach(photoLoader.FilteredCollection, id: \.self) { id in
                        Button {
                            handleCameraClosing(photo: photoLoader.Collection[id])
                        } label: {
                            Image(uiImage: (photoLoader.Collection[id].Image ?? UIImage(systemName: "photo"))!)
                                .resizable()
                                .scaledToFit()
                        }
                    }
                }
            }
        }
        .padding(/*@START_MENU_TOKEN@*/.all/*@END_MENU_TOKEN@*/)
        .sheet(isPresented: $cameraOpen) {
            ZStack {
                CameraPreview(capturedPhoto: $image, photoTrigger: $photoTrigger, photoTaken: $freshPhoto)
                VStack {
                    Spacer()
                    HStack {
                        Spacer()
                        Button(action: {
                            photoTrigger = true
                            cameraOpen = false
                            do {
                                newTemp = try tempPhoto()
                                newMeta = MetaPhoto(tmplt: newTemp!)
                                for _ in 0..<photoLoader.TagList.count {
                                    selectedTags.append(false)
                                }
                                
                            }
                            catch {}
                        }) {
                            Circle()
                                .fill(Color.white)
                                .frame(width: 70, height: 70)
                        }
                        Spacer()
                    }
                }
            }
        }
        .sheet(isPresented: $freshPhoto) {
            PhotoDetailView(
                image: $image,
                photo: $newMeta,
                new: $freshPhoto,
                allTags: photoLoader.TagList,
                selectedTags: $selectedTags,
                onSave: {
                    if let img = image {
                        SaveNewPhoto(img: img, meta: newMeta!)
                    }
                    image = nil
                    newTemp = nil
                    newMeta = nil
                    freshPhoto = false
                }
            )
        }
        .sheet(isPresented: $showingDetails) {
            PhotoDetailView(
                image: $image,
                photo: $selectedMetaPhoto,
                new: $freshPhoto,
                allTags: photoLoader.TagList,
                selectedTags: $selectedTags,
                onSave: {
                    updatePhotoMetadata(meta: selectedMetaPhoto!)
                    selectedMetaPhoto = nil
                    showingDetails = false
                }
            )
        }
    }
    
    func handleCameraClosing(photo: Photo) {
        selectedMetaPhoto = photo.Meta
        image = photo.Image
        var j = 0
        for i in 0..<photoLoader.TagList.count {
            if j < selectedMetaPhoto?.Tags.count ?? 0 && photoLoader.TagList[i].id == selectedMetaPhoto?.Tags[j].id {
                selectedTags.append(true)
                j += 1
            }
            else {selectedTags.append(false)}
        }
        showingDetails = true
    }
    
    func SaveNewPhoto(img: UIImage, meta: MetaPhoto) {
        print("Сохраняется фото+метаданные")
        photoLoader.AppendPhoto(img: img, meta: meta)
        selectedTags = []
    }
    
    func updatePhotoMetadata(meta: MetaPhoto) {
        // поиск по id
        print(meta)
        let idx = photoLoader.getIdxByPhotoID(id: meta.id)
        selectedTags = []
        if idx != -1 {
            photoLoader.Collection[idx].Meta.Name = meta.Name
            photoLoader.Collection[idx].Meta.Description = meta.Description
            photoLoader.Collection[idx].Meta.Tags = []
            meta.Tags.forEach { tag in
                photoLoader.Collection[idx].Meta.Tags.append(tag)
            }
        }
        Task {
            print("Сохраняются метаданные")
            do { try await photoLoader.SavePhotos() }
            catch { print("Error updating metadata: \(error)") }
        }
    }
}

/*
struct Task4View_Previews: PreviewProvider {
    static var previews: some View {
        Task4View()
    }
}
*/
